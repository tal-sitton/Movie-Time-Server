from enum import Enum
from typing import List

import requests

from Screening import Screening
from consts import movies, MovieType, Districts, LanguageType


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
    movies_ids = {movie.get("id"): movie.get("name") for movie in data.get("films")}
    return movies_ids, data.get("events")


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


def find_dubbed(movie_type: list):
    if "dubbed" in movie_type:
        return LanguageType.DUBBED
    elif "subbed" in movie_type:
        return LanguageType.SUBBED
    return LanguageType.UNKNOWN


def get_by_location(location: Locations, date: str, format_date: str, s: requests.Session):
    print("STARTED RAV HEN ", location.name)
    movies_ids, events = prepare(location, date, s)
    for event in events:
        movie_name = movies_ids.get(event.get("filmId"))
        m_time = ":".join(event.get("eventDateTime").split("T")[1].split(":")[:2])
        link = event.get("bookingLink")
        move_type = find_type(event['attributeIds'])
        dubbed = find_dubbed(event.get("attributeIds"))
        movies.append(
            Screening(format_date, "רב חן", location.value['name'], location.value['dis'], movie_name,
                      move_type, m_time, link, location.value['coords'], dubbed)
        )
    print("DONE")


def get_movies(year: str, month: str, day: str, s: requests.Session):
    print("STARTED RAV HEN")
    date = "{}-{}-{}".format(year, month.zfill(2), day.zfill(2))
    format_date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)
    for location in Locations:
        get_by_location(location, date, format_date, s)
    print("DONE RAV HEN")
