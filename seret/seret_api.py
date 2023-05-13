import dataclasses
import difflib
import re
import time
from typing import List, Dict, Tuple

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


def rate_urls(wanted_movie: str, urls: List[Tag], previous_rating: Dict[str, Tuple[int, str]], rating: int = None):
    for url in urls:
        if url.find("h3"):
            name = url.find("h3").text
        else:
            continue
        name = re.sub(r"Seret.co.il| :: |אתר סרט|\|", "", name, flags=re.I).strip().strip("-").strip()
        name = remove_date(name).strip()
        url = url.get("href").replace("/url?q=", "").replace("%3F", "?").replace("%3D", "=").replace("%26", "&")
        if "ביקורת" in name or not url.startswith("https://www.seret.co.il/movies"):
            continue

        diff = difflib.SequenceMatcher(None, name, wanted_movie).ratio()
        rate = rating
        if diff > 0.98:
            if rating:
                rate = 3
            else:
                rate = 2
        elif not rating:
            rate = diff
        elif diff < 0.3:
            continue
        previous_rating[url] = (previous_rating.get(url, (0, ""))[0] + rate, name)
    return previous_rating


def _choose_seret_url(wanted_movie: str, all_movies_urls: List[Tag], recent_urls: List[Tag]) -> str | None:
    title_urls = rate_urls(wanted_movie, recent_urls, {}, 1)
    title_urls = rate_urls(wanted_movie, all_movies_urls, title_urls)
    closest_urls = sorted(title_urls.keys(), key=lambda x: title_urls[x][0], reverse=True)
    if not closest_urls:
        return None
    elif difflib.SequenceMatcher(None, wanted_movie, title_urls[closest_urls[0]][1]).ratio() < 0.3:
        return ""
    return closest_urls[0]


def _get_seret_url(session: requests.Session, movie_name: str) -> str:
    global last_search_request
    if (time.time() - last_search_request) < 1:
        time.sleep(1 - (time.time() - last_search_request))

    session.headers[
        "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"

    base_search = f"https://www.startpage.com/sp/search"
    try:
        res = session.post(base_search, data={"query": f"{movie_name} site:www.seret.co.il", "with_date": "y"})
    except requests.exceptions.ChunkedEncodingError:
        return None
    bs = BeautifulSoup(res.text, "html.parser")
    recent_movies_urls = bs.find_all("a", {"href": re.compile(".*https://seret.co.il/movies/s_movies.asp.*")})

    time.sleep(0.3)

    last_search_request = time.time()
    try:
        res = session.post(base_search, data={"query": f"{movie_name} site:seret.co.il"})
    except requests.exceptions.ChunkedEncodingError:
        return None

    bs = BeautifulSoup(res.text, "html.parser")
    all_movies_urls = bs.find_all("a", {"href": re.compile(".*https://www.seret.co.il/movies/s_movies.asp.*")})
    return _choose_seret_url(movie_name, all_movies_urls, recent_movies_urls)


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

    if url == "":
        return Movie(movie_name, DEFAULT_DESCRIPTION, None, "")

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
