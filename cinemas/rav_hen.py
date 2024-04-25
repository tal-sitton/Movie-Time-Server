import json
import logging
import re
from enum import Enum
from typing import List

import requests

from models import Screening
from models import MovieType, Districts, LanguageType


class Locations(Enum):
    """
    locations and codes
    """
    GIVATAIM = {
        "code": "1058",
        "name": "גבעתיים",
        "dis": Districts.DAN,
        "coords": (32.0663, 34.8107),
    }
    DIZINGOF = {
        "code": "1071",
        "name": "דיזינגוף",
        "dis": Districts.DAN,
        "coords": (32.0783, 34.7736),
    }
    MODIIN = {
        "code": "1069",
        "name": "מודיעין",
        "dis": Districts.JERUSALEM,
        "coords": (31.8998, 35.0076),
    }
    KIRYAT_ONO = {
        "code": "1062",
        "name": "קריית אונו",
        "dis": Districts.DAN,
        "coords": (32.0556, 34.8633),
    }


def prepare(location: Locations, date: str, s: requests.Session) -> tuple:
    url = f"https://www.rav-hen.co.il/rh/data-api-service/v1/quickbook/10104/film-events/in-cinema/{location.value['code']}/at-date/{date}"
    res = s.get(url)
    data = dict(res.json().get("body"))
    movies_data = {movie.get("id"): movie for movie in data.get("films")}
    return movies_data, data.get("events")


def find_type(attributes: List[str]) -> MovieType:
    if "2d" in attributes:
        return MovieType.m_2D
    elif "3d" in attributes:
        return MovieType.m_3D
    elif "4dx" in attributes:
        return MovieType.m_4DX
    elif "imax" in attributes:
        return MovieType.m_IMAX
    elif "vip" in attributes:
        return MovieType.m_VIP
    elif "screenx" in attributes:
        return MovieType.m_SCREENX
    else:
        return MovieType.unknown


def find_dubbed(movie_type: list) -> LanguageType:
    if "dubbed" in movie_type:
        return LanguageType.DUBBED
    elif "subbed" in movie_type:
        return LanguageType.SUBBED
    return LanguageType.UNKNOWN


cached_english_names = {}

logger = logging.getLogger(__name__)


def get_english_name(movie_url: str, s: requests.Session) -> str | None:
    if movie_url in cached_english_names:
        return cached_english_names[movie_url]
    try:
        res = s.get(movie_url)
        raw = re.search("var filmDetails = (.*);", res.text).group(1)
        data: dict = json.loads(raw)
        title = data.get("originalName")
        cached_english_names[movie_url] = title
        return title
    except Exception as e:
        logger.exception(f"Failed to get english name for {movie_url}", exc_info=e)
        return None


def get_by_location(location: Locations, date: str, format_date: str, s: requests.Session) -> list[Screening]:
    logger.info(f"STARTED RAV HEN {location.name}")
    screenings: list[Screening] = []

    movies_data, events = prepare(location, date, s)
    for event in events:
        movie_info = movies_data.get(event.get("filmId"))
        movie_name = movie_info.get('name')
        m_time = ":".join(event.get("eventDateTime").split("T")[1].split(":")[:2])
        link = event.get("bookingLink")
        move_type = find_type(event['attributeIds'])
        dubbed = find_dubbed(event.get("attributeIds"))
        english_name = get_english_name(movie_info.get("link"), s)
        screenings.append(
            Screening(format_date, "רב חן", location.value['name'], location.value['dis'], movie_name,
                      english_name, move_type, m_time, link, location.value['coords'], dubbed)
        )
    logger.info(f"DONE RAV HEN {location.name}")
    return screenings


def get_screenings(year: str, month: str, day: str, s: requests.Session) -> List[Screening]:
    logger.info("STARTED RAV HEN")
    screenings: List[Screening] = []
    date = "{}-{}-{}".format(year, month.zfill(2), day.zfill(2))
    format_date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)

    for location in Locations:
        screenings.extend(get_by_location(location, date, format_date, s))
    logger.info("DONE RAV HEN")
    return screenings
