from enum import Enum
from typing import Dict

import requests

from Screening import Screening
from consts import screenings, Districts, MovieType, LanguageType


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


def get_by_location(location: Locations, date: str, format_date: str, s: requests.Session):
    print("STARTED Movie Land ", location.name)
    if location.name not in cache:
        url = f"https://www.movieland-cinema.co.il/api/Events?&TheatreId={location.value['TheatreId']}" \
              f"&isForSelectedTheaterOnly=true&isHideVODRent=true"
        res = s.get(url)
        if not res.ok:
            return
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
            screenings.append(
                Screening(format_date, "מובילנד", location.value["name"], location.value['dis'], movie_name,
                          movie_type, time, link, location.value['coords'], dubbed)
            )

    print("DONE")


def get_screenings(year: str, month: str, day: str, s: requests.Session):
    print("STARTED Movie Land")
    date = "{}.{}".format(day.zfill(2), month.zfill(2))
    format_date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)
    for location in Locations:
        get_by_location(location, date, format_date, s)
    print("DONE Movie Land")
