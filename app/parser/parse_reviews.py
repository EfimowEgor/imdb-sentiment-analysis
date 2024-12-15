import os
from review.review import Review

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


def sanitize_url(url: str) -> str:
    reviews_url = '/'.join(url.split('/')[:-1]) + "/reviews"

    return reviews_url

async def get_reviews(url: str, headers: dict[str, str], max_reviews=float('inf')) -> list[dict]:
    try:
        review_collection = Review()

        url = sanitize_url(url)

        print(f"The processed URL is: {url}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=headers["User-Agent"]
            )
            
            page = await context.new_page()
            await page.goto(url)

            already_scraped_titles = set()

            while len(review_collection) < max_reviews:
                await page.wait_for_selector("div[data-testid='review-card-parent']", timeout=10000)

                spoiler_buttons = page.locator(".review-spoiler-button")
                count = await spoiler_buttons.count()
                for _ in range(count):
                    try:
                        await spoiler_buttons.nth(0).click()
                        await page.wait_for_timeout(200) 
                    except:
                        pass
                
                current_review_count = len(await page.locator("div[data-testid='review-card-parent']").all())


                html = await page.content()
                soup = BeautifulSoup(html, "html.parser")
                review_cards = soup.find_all("div", {"data-testid": "review-card-parent"})

                for card in review_cards[:current_review_count]:
                    rating_elem = card.find("span", class_="ipc-rating-star--rating")
                    title_elem = card.find("h3", class_="ipc-title__text")

                    if not rating_elem or not title_elem:
                        continue

                    rating = rating_elem.text
                    title = title_elem.text.strip()

                    if title in already_scraped_titles: 
                        continue

                    already_scraped_titles.add(title)

                    review_text_element = card.find("div", {"class": "ipc-html-content-inner-div"}) 
                    if not review_text_element:
                        review_text_element = card.find("div", {"class": lambda x: x and "review-spoiler__content" in x})
                    review_text = review_text_element.text.strip() if review_text_element else "N/A"
                    if title in review_text:
                        review_text = review_text.replace(title, '').strip()

                    review_collection.add_review(rating, title, review_text)

                    if len(review_collection) >= max_reviews:
                        break

                if len(review_collection) >= max_reviews:
                    break

                try:
                    load_more_button = page.locator("button", has_text="25 more")
                    clicked = await load_more_button.click()

                    if clicked:
                        await page.wait_for_selector(
                            f"div[data-testid='review-card-parent']:nth-child({current_review_count + 1})", 
                            state="attached", timeout=10000)
                except Exception as e:
                    print(f"Error clicking 'Load More': {e}")
                    break

            await browser.close()

        return review_collection.reviews
    
    except Exception as e:
        print(f"Error: {e}")
