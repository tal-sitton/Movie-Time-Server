from enum import Enum

import requests

from Screening import Screening
from consts import MovieType, movies, Districts


class Locations(Enum):
    """
    locations and codes
    """
    RISHON = {
        "code": "1072",
        "name": "ראשון לציון",
        "dis": Districts.DAN,
    }
    AYALON = {
        "code": "1025",
        "name": "קניון אילון",
        "dis": Districts.DAN,
    }
    ZICHRON = {
        "code": "1075",
        "name": "זכרון יעקב",
        "dis": Districts.ZAFON,
    }
    HAIFA = {
        "code": "1070",
        "name": "חיפה",
        "dis": Districts.ZAFON,
    }
    JERUSALEM = {
        "code": "1073",
        "name": "ירושלים",
        "dis": Districts.JERUSALEM,
    }
    BEER_SHEVA = {
        "code": "1074",
        "name": "באר שבע",
        "dis": Districts.DAROM,
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


def prepare(location: Locations, date: str, s: requests.Session) -> tuple:
    url = f"https://www.yesplanet.co.il/il/data-api-service/v1/quickbook/10100/film-events/in-cinema/{location.value['code']}/at-date/{date}"
    res = s.get(url)
    data = dict(res.json().get("body"))
    movies_ids = {movie.get("id"): movie.get("name") for movie in data.get("films")}
    return movies_ids, data.get("events")


def get_by_location(location: Locations, date: str, format_date: str, s: requests.Session):
    print("STARTED YES PLANET ", location.name)
    movies_ids, events = prepare(location, date, s)
    for event in events:
        movie_name = movies_ids.get(event.get("filmId")).replace("עברית עם כתוביות ", "").strip()
        m_time = ":".join(event.get("eventDateTime").split("T")[1].split(":")[:2])
        movie_type = find_type(event.get("attributeIds"))
        link = event.get("bookingLink")
        movies.append(
            Screening(format_date, "יס פלאנט", location.value['name'], location.value['dis'], movie_name,
                      movie_type, m_time, link)
        )
    print("DONE")


def get_movies(year: str, month: str, day: str, s: requests.Session):
    print("STARTED YES PLANET")
    date = "{}-{}-{}".format(year, month.zfill(2), day.zfill(2))
    format_date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)
    for location in Locations:
        get_by_location(location, date, format_date, s)
    print("DONE YES PLANET")
