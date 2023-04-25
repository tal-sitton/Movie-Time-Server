import dataclasses
import difflib
import re
import time
from typing import List, Dict

import requests
from bs4 import BeautifulSoup, Tag

from seret.imdb_api import get_imdb_rating

last_search_request = 0

SEARCH_RETRIES = 5

DEFAULT_DESCRIPTION = "לא נמצא תיאור"

FIRST_HEBREW_CHAR = ord('א')
LAST_HEBREW_CHAR = ord('ת')

FIRST_ENGLISH_CHAR = ord('a')
LAST_ENGLISH_CHAR = ord('z')


@dataclasses.dataclass
class Movie:
    name: str
    description: str
    rating: float | None
    image_url: str

    def to_dict(self) -> dict:
        return self.__dict__


def is_acceptable_language(name: str) -> bool:
    for char in re.findall("\w", name):
        char = char.lower()
        if not FIRST_HEBREW_CHAR <= ord(char) <= LAST_HEBREW_CHAR \
                and not FIRST_ENGLISH_CHAR <= ord(char) <= LAST_ENGLISH_CHAR \
                and not char.isdigit():
            return False
    return True


def remove_date(name: str) -> str:
    return re.sub(r"\(\d{4}\)$", "", name).strip()


def _choose_seret_url(urls: List[Tag], wanted_movie: str) -> str | None:
    title_urls: Dict[str: str] = {}
    for url in urls:
        if url.find("h3"):
            name = url.find("h3").text
        elif url.findChild("span", recursive=False, string=re.compile("\w*")):
            name = url.findChild("span", recursive=False, string=re.compile("\w*")).text
        elif url.text:
            name = url.text
        else:
            continue

        name = name.replace("::", "")
        name = name.replace("Seret.co.il", "")
        name = name.replace("סרט", "")
        name = remove_date(name)
        url = url.get("href").replace("/url?q=", "").replace("%3F", "?").replace("%3D", "=").replace("%26", "&")
        if "ביקורת" in name or not url.startswith("https://www.seret.co.il/movies"):
            continue
        title_urls[name] = url
    closest_names = sorted(title_urls.keys(), key=lambda x: difflib.SequenceMatcher(None, x, wanted_movie).ratio(),
                           reverse=True)
    if not closest_names:
        return None
    return title_urls[closest_names[0]]


def _get_seret_url(session: requests.Session, movie_name: str) -> str:
    global last_search_request
    if (time.time() - last_search_request) < 1:
        time.sleep(1 - (time.time() - last_search_request))

    search = f"https://www.bing.com/search?q={movie_name} site:www.seret.co.il"
    session.headers[
        "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    last_search_request = time.time()
    try:
        res = session.get(search)
    except requests.exceptions.ChunkedEncodingError:
        return None

    bs = BeautifulSoup(res.text, "html.parser")
    urls = bs.find_all("a", {"href": re.compile(".*https://www.seret.co.il/movies/s_movies.asp.*")})
    return _choose_seret_url(urls, movie_name)


def _get_names(bs: BeautifulSoup) -> List[str]:
    return [
        remove_date(bs.find("span", {"itemprop": "name"}).text),
        remove_date(bs.find("span", {"itemprop": "alternatename"}).text)
    ]


def _get_description(bs: BeautifulSoup) -> str:
    return bs.find("span", {"itemprop": "description"}).text


def _get_image_url(bs: BeautifulSoup) -> str:
    temp = bs.find("div", {"class": "picnotice"})
    return temp.parent.find("img").get("data-src").replace("../", "https://www.seret.co.il/")


def _get_year(bs: BeautifulSoup) -> int:
    return int(bs.find("span", {"itemprop": "dateCreated"}).text)


def _get_rating(session: requests.Session, movie_name: str, year: int) -> float | None:
    score = get_imdb_rating(session, movie_name, year)
    return score


def _is_canonical_version(bs: BeautifulSoup, original_url: str):
    return not bs.find("link", {"rel": "canonical"}) or bs.find("link", {"rel": "canonical"})[
        "href"] == original_url


def get_info(session: requests.Session, movie_name: str, retries=0) -> Movie:
    if not is_acceptable_language(movie_name):
        return Movie(movie_name, DEFAULT_DESCRIPTION, None, "")
    url = _get_seret_url(session, movie_name)

    if not url:
        if retries > SEARCH_RETRIES:
            return Movie(movie_name, DEFAULT_DESCRIPTION, None, "")
        print(f"Trying again {movie_name} - {retries}/{SEARCH_RETRIES}")
        return get_info(session, movie_name, retries + 1)

    res = session.get(url)
    res.encoding = "windows-1255"
    bs = BeautifulSoup(res.text, "html.parser")
    is_canonical = _is_canonical_version(bs, url)

    if not is_canonical:
        new_url = bs.find("link", {"rel": "canonical"})["href"]
        res = session.get(new_url)
        res.encoding = "windows-1255"
        bs = BeautifulSoup(res.text, "html.parser")

    hebrew, english = _get_names(bs)

    description = _get_description(bs)
    image_url = _get_image_url(bs)
    rating = _get_rating(session, english, _get_year(bs))
    return Movie(hebrew, description, rating, image_url)
