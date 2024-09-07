import json
import logging
import re
from enum import Enum

import requests

from models import MovieType, Districts, LanguageType
from models import Screening
from proxy import ProxifiedSession


class Locations(Enum):
    """
    locations and codes
    """
    RISHON = {
        "code": "1072",
        "name": "ראשון לציון",
        "dis": Districts.DAN,
        "coords": (31.9798, 34.7475),
    }
    AYALON = {
        "code": "1025",
        "name": "קניון אילון",
        "dis": Districts.DAN,
        "coords": (32.0995, 34.8272),
    }
    ZICHRON = {
        "code": "1075",
        "name": "זכרון יעקב",
        "dis": Districts.ZAFON,
        "coords": (32.5697, 34.9333),
    }
    HAIFA = {
        "code": "1070",
        "name": "חיפה",
        "dis": Districts.ZAFON,
        "coords": (32.7937, 35.0383),
    }
    JERUSALEM = {
        "code": "1073",
        "name": "ירושלים",
        "dis": Districts.JERUSALEM,
        "coords": (31.7624, 35.2257),
    }
    BEER_SHEVA = {
        "code": "1074",
        "name": "באר שבע",
        "dis": Districts.DAROM,
        "coords": (31.2244, 34.8010),
    }


def find_type(movie_type: list):
    if "4dx" in movie_type:
        return MovieType.m_4DX
    if "vip" in movie_type:
        return MovieType.m_VIP
    elif "imax" in movie_type:
        return MovieType.m_IMAX
    elif "3D" in movie_type:
        return MovieType.m_3D
    elif "screenx" in movie_type:
        return MovieType.m_SCREENX
    else:
        return MovieType.m_2D


def find_dubbed(movie_info: list) -> LanguageType:
    if "dubbed" in movie_info:
        return LanguageType.DUBBED
    elif "subbed" in movie_info:
        return LanguageType.SUBBED
    return LanguageType.UNKNOWN


cached_english_names = {}

logger = logging.getLogger(__name__)


def get_english_name(movie_url: str, s: requests.Session) -> str | None:
    if movie_url in cached_english_names:
        return cached_english_names[movie_url]
    res = None
    try:
        res = s.get(movie_url)
        raw = re.search("var filmDetails = (.*);", res.text).group(1)
        data: dict = json.loads(raw)
        title = data.get("originalName")
        cached_english_names[movie_url] = title
        return title
    except Exception as e:
        logger.exception(f"Failed to get english name for {movie_url}", exc_info=e)
        if res:
            logger.info(res.text)
        return None


def prepare(location: Locations, date: str, s: requests.Session) -> tuple:
    url = f"https://www.planetcinema.co.il/il/data-api-service/v1/quickbook/10100/film-events/in-cinema/{location.value['code']}/at-date/{date}"
    res = s.get(url)
    try:
        data = dict(res.json().get("body"))
        movies_data = {movie.get("id"): movie for movie in data.get("films")}
        return movies_data, data.get("events")
    except Exception as e:
        logger.info(url)
        logger.info(res.text)
        raise e


def get_by_location(location: Locations, date: str, format_date: str, s: requests.Session) -> list[Screening]:
    logger.info(f"STARTED YES PLANET {location.name}")
    screenings: list[Screening] = []

    movies_data, events = prepare(location, date, s)
    for event in events:
        movie_info = movies_data.get(event.get("filmId"))
        movie_name = movie_info.get("name")
        m_time = ":".join(event.get("eventDateTime").split("T")[1].split(":")[:2])
        movie_type = find_type(event.get("attributeIds"))
        link = event.get("bookingLink")
        dubbed = find_dubbed(event.get("attributeIds"))
        english_name = get_english_name(movie_info.get("link"), s)
        screenings.append(
            Screening(format_date, "יס פלאנט", location.value['name'], location.value['dis'], movie_name,
                      english_name, movie_type, m_time, link, location.value['coords'], dubbed))
    logger.info(f"DONE YES PLANET {location.name}")
    return screenings


def get_screenings(year: str, month: str, day: str, s: requests.Session) -> list[Screening]:
    logger.info("STARTED YES PLANET")
    screenings: list[Screening] = []
    date = "{}-{}-{}".format(year, month.zfill(2), day.zfill(2))
    format_date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)

    with ProxifiedSession(s) as ps:
        for location in Locations:
            try:
                screenings.extend(get_by_location(location, date, format_date, ps))
            except Exception as e:
                logger.exception(f"Failed to get screenings for {location.name}", exc_info=e)

    logger.info("DONE YES PLANET")
    return screenings


if __name__ == '__main__':
    from datetime import datetime

    s = requests.Session()
    print(get_screenings(str(datetime.now().year), str(datetime.now().month).zfill(2),
                         str(datetime.now().day + 1).zfill(2), s))
