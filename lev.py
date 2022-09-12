from enum import Enum

import requests

import consts
from Screening import Screening
from consts import movies, Districts


class Locations(Enum):
    """
    locations and codes
    """
    TEL_AVIV = {
        "code": "1150",
        "name": "תל אביב",
        "dis": Districts.DAN,
        "coords": (32.0748, 34.7755),
    }
    RAMAT_HASHARON = {
        "code": "1162",
        "name": "רמת השרון",
        "dis": Districts.SHARON,
        "coords": (32.1492, 34.8397),
    }
    MANDARIN = {
        "code": "1156",
        "name": "מנדרין",
        "dis": Districts.DAN,
        "coords": (32.1435, 34.7931),
    }
    EVEN_YEHUDA = {
        "code": "1151",
        "name": "אבן יהודה",
        "dis": Districts.SHARON,
        "coords": (32.2692, 34.8906),
    }
    SMADAR = {
        "code": "1158",
        "name": "סמדר",
        "dis": Districts.JERUSALEM,
        "coords": (31.7648, 35.2221),
    }
    RAANANA = {
        "code": "1161",
        "name": "רעננה",
        "dis": Districts.SHARON,
        "coords": (32.1840, 34.8531),
    }
    OMER = {
        "code": "1155",
        "name": "עומר",
        "dis": Districts.DAROM,
        "coords": (31.2632, 34.8475),
    }
    SHOHAM = {
        "code": "1159",
        "name": "שוהם",
        "dis": Districts.DAN,
        "coords": (31.9993, 34.9470),
    }
    DANIEL = {
        "code": "1154",
        "name": "דניאל",
        "dis": Districts.SHARON,
        "coords": (32.1715, 34.8005),
    }


def get_by_location(location: Locations, date: str, format_date: str, s: requests.Session):
    print("STARTED LEV ", location.name)
    url = f"https://ticket.lev.co.il/api/presentations?locationId={location.value['code']}&includeSynopsis=0"
    res = s.get(url)
    for movie in res.json()['presentations']:
        if date not in movie['dateTime']:
            continue
        name = movie['featureName'].replace(" מדובב", "").replace(" אנגלית", "").strip()
        time = movie['dateTime'].split(" ")[1]
        link = f"https://ticket.lev.co.il/order/{movie['id']}"
        movies.append(
            Screening(format_date, "לב", location.value["name"], location.value['dis'], name, consts.MovieType.m_2D,
                      time, link, location.value['coords'])
        )
    print("DONE")


def get_movies(year: str, month: str, day: str, s: requests.Session):
    print("STARTED LEV")
    date = "{}-{}-{}".format(year, month.zfill(2), day.zfill(2))
    format_date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)
    for location in Locations:
        get_by_location(location, date, format_date, s)
    print("DONE LEV")
