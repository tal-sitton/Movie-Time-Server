import logging
from enum import Enum
from typing import Dict

import requests
from bs4 import BeautifulSoup

from models import Districts, MovieType, LanguageType
from models import Screening


class Locations(Enum):
    """
    locations and codes
    """
    CARMIEL = {
        "TheatreId": "1290",
        "name": "כרמיאל",
        "dis": Districts.ZAFON,
        "coords": (32.9220, 35.3078),
    }
    HAIFA = {
        "TheatreId": "1291",
        "name": "חיפה",
        "dis": Districts.ZAFON,
        "coords": (32.7894, 34.9639),
    }
    NATANYA = {
        "TheatreId": "1292",
        "name": "נתניה",
        "dis": Districts.SHARON,
        "coords": (32.2812, 34.8620),
    }


cache = {}

logger = logging.getLogger(__name__)


def find_type(info: Dict[str, str | bool]) -> MovieType:
    if info.get("IsVip"):
        return MovieType.m_VIP
    if info.get("ThreeD"):
        return MovieType.m_3D
    return MovieType.unknown


def find_dubbed(info: Dict[str, str | bool]) -> LanguageType:
    if info.get("Dubbed"):
        return LanguageType.DUBBED
    return LanguageType.UNKNOWN


cached_english_names = {}


def get_english_name(movie_id: str, s: requests.Session) -> str | None:
    if movie_id in cached_english_names:
        return cached_english_names[movie_id]
    url = f"https://www.movieland-cinema.co.il/movie/{movie_id}"
    try:
        bs = BeautifulSoup(s.get(url).text, "html.parser")
        title = bs.find("div", {"class": "bg-more-b"}).find_all("span")[1].text
        cached_english_names[movie_id] = title
        return title
    except Exception as e:
        logger.exception(f"Failed to get english name for {movie_id}", exc_info=e)
        return None


def get_by_location(location: Locations, date: str, format_date: str, s: requests.Session) -> list[Screening]:
    logger.info(f"STARTED Movie Land {location.name}")
    screenings: list[Screening] = []

    if location.name not in cache:
        url = f"https://www.movieland-cinema.co.il/api/Events?&TheatreId={location.value['TheatreId']}" \
              f"&isForSelectedTheaterOnly=true&isHideVODRent=true"
        res = s.get(url)
        if not res.ok:
            return []
        res = res.json()
        cache[location.name] = res
    else:
        res = cache[location.name]

    filtered_movies = {}
    for movie in res:
        shows = [movie_date for movie_date in movie.get("Dates") if
                 date in movie_date.get("Day")]
        if shows:
            filtered_movies[movie.get("Name")] = shows

    for movie_name, shows in filtered_movies.items():
        for show in shows:
            time = show.get("Hour")
            link = show.get("BookingNativeUrl")
            movie_type = find_type(show)
            dubbed = find_dubbed(show)
            movie_id = show.get("MovieId")
            english_name = get_english_name(movie_id, s)
            screenings.append(
                Screening(format_date, "מובילנד", location.value["name"], location.value['dis'], movie_name,
                          english_name, movie_type, time, link, location.value['coords'], dubbed)
            )

    logger.info(f"DONE Movie Land {location.name}")
    return screenings


def get_screenings(year: str, month: str, day: str, s: requests.Session) -> list[Screening]:
    logger.info("STARTED Movie Land")
    screenings: list[Screening] = []
    date = "{}.{}".format(day.zfill(2), month.zfill(2))
    format_date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)

    for location in Locations:
        screenings.extend(get_by_location(location, date, format_date, s))
    logger.info("DONE Movie Land")
    return screenings


if __name__ == '__main__':
    from datetime import datetime

    s = requests.Session()
    print(get_screenings(str(datetime.now().year), str(datetime.now().month).zfill(2),
                         str(datetime.now().day + 1).zfill(2), s))
