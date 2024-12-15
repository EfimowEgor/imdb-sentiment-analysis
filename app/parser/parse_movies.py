import requests
from bs4 import BeautifulSoup


def get_top_movies(base_path: str, url: str, headers: dict[str, str], limit: int = 10):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    movies = []
    movie_path = "li.ipc-metadata-list-summary-item.sc-4929eaf6-0.DLYcv.cli-parent a.ipc-title-link-wrapper"
    
    rows = soup.select(movie_path)[:limit]
    for row in rows:
        title = row.text
        link = base_path + row["href"]
        movies.append((title, link))
    return movies