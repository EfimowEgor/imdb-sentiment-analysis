import asyncio

from parse_movies import get_top_movies
from parse_reviews import get_reviews
from config import Settings

import pandas as pd


async def process_reviews(url: str, headers: dict, reviews_count: int) -> list[dict]:
    reviews = await get_reviews(url, headers, reviews_count)
    print(f"Fetched reviews for {url}")
    return reviews

async def run():
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    movies = get_top_movies(settings.base_path, 
                            settings.chart_path,
                            HEADERS)
    
    df = pd.DataFrame(columns=["rating", "title", "review"])

    tasks = [
        asyncio.create_task(process_reviews(url, HEADERS, settings.reviews_count)) 
        for _, url in movies
    ]

    for completed_task in asyncio.as_completed(tasks):
        try:
            reviews = await completed_task
            if reviews:
                tmp = pd.DataFrame(reviews)
                df = pd.concat([df, tmp], ignore_index=True)
                print(f"DataFrame updated, current size: {len(df)}")
        except Exception as e:
            print(f"Error processing task: {e}")

    save_path = settings.data_path
    df.to_csv(save_path, index=False)


if __name__ == "__main__":
    settings = Settings()
    asyncio.run(run())
