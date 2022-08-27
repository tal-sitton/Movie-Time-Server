from enum import Enum

import bs4
import requests

from Screening import Screening
from consts import movies, MovieType


class Locations(Enum):
    """
    locations and codes
    """
    MODIIN = {
        "code": "MOD",
        "code2": "1",
        "name": "מודיעין"
    }
    KIRYON = {
        "code": "KIRYON",
        "code2": "2",
        "name": "קריון"
    }
    KFAR_SABBA = {
        "code": "KS",
        "code2": "16",
        "name": "כפר סבא"
    }
    HAIFA = {
        "code": "HAIFA",
        "code2": "9",
        "name": "חיפה"
    }
    PETACH_TIKVA = {
        "code": "PT",
        "code2": "14",
        "name": "פתח תקווה"
    }
    RECHOVOT = {
        "code": "RH",
        "code2": "17",
        "name": "רחובות"
    }
    ASHKELON = {
        "code": "ASHK",
        "code2": "8",
        "name": "אשקלון"
    }
    KARMIEL = {
        "code": "KAR",
        "code2": "15",
        "name": "כרמיאל"
    }
    NAHARIA = {
        "code": "NHR",
        "code2": "6",
        "name": "נהריה"
    }
    ASHDOD = {
        "code": "ASHDOD",
        "code2": "5",
        "name": "אשדוד"
    }


def get_by_location(location: Locations, date: str, formatted_date: str, s: requests.Session):
    print("STARTED HOT CINEMA ", location.name)
    url = f"https://tix.hotcinema.co.il/{location.value['code']}/TicketingTodaysEventsPageRes.aspx?BusinessDate={date}"
    res = s.get(url)
    bs = bs4.BeautifulSoup(res.text, "html.parser")
    movies_data = bs.find_all("div", {"class": "item"})

    for data in movies_data:
        name = data.find(class_="movieName").text
        info = data.find(class_="times").text.strip()
        for time in info.split("\n")[2:]:
            movies.append(Screening(formatted_date, "Hot Cinema", location.value['name'], name, MovieType.m_2D, time,
                                    f"https://hotcinema.co.il/theater/{location.value['code2']}"))


def get_movies(year: str, month: str, day: str, s: requests.Session):
    print("STARTED HOT CINEMA")
    formatted_date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)
    date = "{}-{}-{}".format(year, month.zfill(2), day.zfill(2))

    for location in Locations:
        get_by_location(location, date, formatted_date, s)
    print("DONE HOT CINEMA")
