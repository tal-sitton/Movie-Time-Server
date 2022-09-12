from enum import Enum

import requests

from Screening import Screening
from consts import movies, MovieType, Districts


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


def get_by_location(location: Locations, date: str, format_date: str, s: requests.Session):
    print("STARTED RAV HEN ", location.name)
    movies_ids, events = prepare(location, date, s)
    for event in events:
        movie_name = movies_ids.get(event.get("filmId"))
        m_time = ":".join(event.get("eventDateTime").split("T")[1].split(":")[:2])
        link = event.get("bookingLink")
        movies.append(
            Screening(format_date, "רב חן", location.value['name'], location.value['dis'], movie_name,
                      MovieType.m_2D, m_time, link, location.value['coords'])
        )
    print("DONE")


def get_movies(year: str, month: str, day: str, s: requests.Session):
    print("STARTED RAV HEN")
    date = "{}-{}-{}".format(year, month.zfill(2), day.zfill(2))
    format_date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)
    for location in Locations:
        get_by_location(location, date, format_date, s)
    print("DONE RAV HEN")
