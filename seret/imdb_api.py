import difflib
import json

import requests
from bs4 import BeautifulSoup

IMDB_API_DATA = "d"
IMDB_API_TITLE = "l"
IMDB_API_YEAR = "y"


def get_title_id(session: requests.Session, name: str, year: int) -> str | None:
    """
    get imdb id of a title
    :param session: session to use
    :param name: name of the title
    :param year: year the title was released
    :return: imdb id of the title
    """
    url = f"https://v3.sg.media-imdb.com/suggestion/x/{name}.json"
    print(url)
    response = session.get(url)
    results = response.json()[IMDB_API_DATA]
    movies = []
    for result in results:
        if result.get(IMDB_API_YEAR) and abs(result[IMDB_API_YEAR] - year) < 2:
            movies.append(result)

    movies.sort(
        key=lambda x: (x[IMDB_API_YEAR] == year, difflib.SequenceMatcher(None, x[IMDB_API_TITLE], name).ratio()),
        reverse=True)
    if not movies:
        return None
    return movies[0]["id"]


def get_title_info(session: requests.Session, title_id: str) -> dict:
    """
    get information about a title
    :param session: session to use
    :param title_id: id of the title
    :return: information given by the API
    """
    url = f"https://www.imdb.com/title/{title_id}"
    response = session.get(url)
    print(url)
    bs = BeautifulSoup(response.text, "html.parser")
    data = bs.find("script", type="application/ld+json")
    return json.loads(data.text)


def get_imdb_rating(session: requests.Session, movie: str, year: int) -> float | None:
    """
    get rating of a movie
    :param session: session to use
    :param movie: name of the movie
    :param year: year the movie was released
    :param retried: if this is the first time to get the rating
    :param id: imdb id of the title
    :return: rating given by the API
    """
    id = get_title_id(session, movie, year)
    if not id:
        return None
    info = get_title_info(session, id)
    return info["aggregateRating"]['ratingValue']


if __name__ == '__main__':
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT)"})
    reting = get_imdb_rating(s, "mario", 2023)
    print(reting)
