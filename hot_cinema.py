from enum import Enum

import requests

from Screening import Screening
from consts import movies, MovieType, Districts, LanguageType


class Locations(Enum):
    """
    locations and codes
    """
    MODIIN = {
        "code": "1",
        "name": "מודיעין",
        "dis": Districts.JERUSALEM,
        "coords": (31.8890, 34.9634),
    }
    KIRYON = {
        "code": "2",
        "name": "קריון",
        "dis": Districts.ZAFON,
        "coords": (32.8427, 35.0897),
    }
    KFAR_SABBA = {
        "code": "16",
        "name": "כפר סבא",
        "dis": Districts.SHARON,
        "coords": (32.1654, 34.9277),
    }
    HAIFA = {
        "code": "9",
        "name": "חיפה",
        "dis": Districts.ZAFON,
        "coords": (32.7896, 35.0071),
    }
    PETACH_TIKVA = {
        "code": "14",
        "name": "פתח תקווה",
        "dis": Districts.DAN,
        "coords": (32.0926, 34.8650),
    }
    RECHOVOT = {
        "code": "17",
        "name": "רחובות",
        "dis": Districts.DAN,
        "coords": (31.8942, 34.8080),
    }
    ASHKELON = {
        "code": "8",
        "name": "אשקלון",
        "dis": Districts.DAROM,
        "coords": (31.6812, 34.5567),
    }
    KARMIEL = {
        "code": "15",
        "name": "כרמיאל",
        "dis": Districts.ZAFON,
        "coords": (32.9276, 35.3263),
    }
    NAHARIA = {
        "code": "6",
        "name": "נהריה",
        "dis": Districts.ZAFON,
        "coords": (32.9902, 35.0953),
    }
    ASHDOD = {
        "code": "5",
        "name": "אשדוד",
        "dis": Districts.DAROM,
        "coords": (31.7931, 34.6386),
    }


def find_dubbed(info: dict):
    if info["DubbedLanguage"] == "עברית":
        return LanguageType.DUBBED
    elif info["SubtitledLanguage"] == "עברית":
        return LanguageType.SUBBED
    return LanguageType.UNKNOWN


def get_by_location(location: Locations, date: str, s: requests.Session):
    print("STARTED HOT CINEMA ", location.name)
    url = f"https://hotcinema.co.il/tickets/TheaterEvents?date={date.replace('-', '%2F')}&theatreid={location.value['code']}"
    res = s.get(url).json()
    for movie_info in res:
        name = movie_info["MovieName"].replace(" אנגלית", "").replace(" עברית", "")
        for m_date in movie_info["Dates"]:
            m_time = m_date["Hour"]
            m_id = m_date["EventId"]
            link = f"https://hotcinema.co.il/order?theaterId={location.value['code']}&eventId={m_id}&site=undefined"
            dubbed = find_dubbed(m_date)
            movies.append(
                Screening(date, "הוט סינמה", location.value['name'], location.value['dis'], name,
                          MovieType.m_3D if m_date['Is3D'] else MovieType.unknown, m_time, link,
                          location.value['coords'], dubbed)
            )
    print("DONE")


def get_movies(year: str, month: str, day: str, s: requests.Session):
    print("STARTED HOT CINEMA")
    date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)

    for location in Locations:
        get_by_location(location, date, s)
    print("DONE HOT CINEMA")
