from enum import Enum

import requests

from Screening import Screening
from consts import movies, MovieType, Districts


class Locations(Enum):
    """
    locations and codes
    """
    MODIIN = {
        "code": "1",
        "name": "מודיעין",
        "dis": Districts.JERUSALEM,
    }
    KIRYON = {
        "code": "2",
        "name": "קריון",
        "dis": Districts.ZAFON,
    }
    KFAR_SABBA = {
        "code": "16",
        "name": "כפר סבא",
        "dis": Districts.SHARON,
    }
    HAIFA = {
        "code": "9",
        "name": "חיפה",
        "dis": Districts.ZAFON,
    }
    PETACH_TIKVA = {
        "code": "14",
        "name": "פתח תקווה",
        "dis": Districts.DAN,
    }
    RECHOVOT = {
        "code": "17",
        "name": "רחובות",
        "dis": Districts.DAN,
    }
    ASHKELON = {
        "code": "8",
        "name": "אשקלון",
        "dis": Districts.DAROM,
    }
    KARMIEL = {
        "code": "15",
        "name": "כרמיאל",
        "dis": Districts.ZAFON,
    }
    NAHARIA = {
        "code": "6",
        "name": "נהריה",
        "dis": Districts.ZAFON,
    }
    ASHDOD = {
        "code": "5",
        "name": "אשדוד",
        "dis": Districts.DAROM,
    }


def get_by_location(location: Locations, date: str, s: requests.Session):
    print("STARTED HOT CINEMA ", location.name)
    url = f"https://hotcinema.co.il/tickets/TheaterEvents?date={date.replace('-', '%2F')}&theatreid={location.value['code']}"
    res = s.get(url).json()
    for movie_info in res:
        name = movie_info["MovieName"]
        for m_date in movie_info["Dates"]:
            m_time = m_date["Hour"]
            m_id = m_date["EventId"]
            link = f"https://hotcinema.co.il/order?theaterId={location.value['code']}&eventId={m_id}&site=undefined"
            movies.append(
                Screening(date, "הוט סינמה", location.value['name'], location.value['dis'], name,
                          MovieType.m_3D if m_date['Is3D'] else MovieType.m_2D, m_time, link)
            )
    print("DONE")


def get_movies(year: str, month: str, day: str, s: requests.Session):
    print("STARTED HOT CINEMA")
    date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)

    for location in Locations:
        get_by_location(location, date, s)
    print("DONE HOT CINEMA")
