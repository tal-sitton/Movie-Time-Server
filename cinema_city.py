from enum import Enum

import requests

import consts
from Screening import Screening
from consts import movies, Districts


class Locations(Enum):
    """
    locations and codes
    """
    GLILOT = {
        "code": "1",
        "TheatreId": "1170",
        "VenueTypeId": "1",
        "name": "גלילות",
        "dis": Districts.DAN,
        "coords": (32.1464, 34.8040),
    }
    RISHON = {
        "code": "2",
        "TheatreId": "1173",
        "VenueTypeId": "1",
        "name": "ראשון לציון",
        "dis": Districts.DAN,
        "coords": (31.9833, 34.7711),
    }
    JERUSALEM = {
        "code": "3",
        "TheatreId": "1174",
        "VenueTypeId": "1",
        "name": "ירושלים",
        "dis": Districts.JERUSALEM,
        "coords": (31.7830, 35.2036),
    }
    KFAR_SABBA = {
        "code": "4",
        "TheatreId": "1175",
        "VenueTypeId": "1",
        "name": "כפר סבא",
        "dis": Districts.SHARON,
        "coords": (32.1728, 34.9297),
    }
    NATANIA = {
        "code": "5",
        "TheatreId": "1176",
        "VenueTypeId": "1",
        "name": "נתניה",
        "dis": Districts.SHARON,
        "coords": (32.2911, 34.8618),
    }
    BEER_SHEVA = {
        "code": "17",
        "TheatreId": "1178",
        "VenueTypeId": "1",
        "name": "באר שבע",
        "dis": Districts.DAROM,
        "coords": (31.2341, 34.7994),
    }
    HADERA = {
        "code": "13",
        "TheatreId": "1350",
        "VenueTypeId": "1",
        "name": "חדרה",
        "dis": Districts.ZAFON,
        "coords": (31.2341, 34.7994),
    }
    ASHDOD = {
        "code": "25",
        "TheatreId": "1181",
        "VenueTypeId": "1",
        "name": "אשדוד",
        "dis": Districts.DAROM,
        "coords": (31.7764, 34.6641),
    }


def get_date(location: Locations, date: str, s: requests.Session):
    date = date.replace("-", "/")
    url = f"https://www.cinema-city.co.il/tickets/GetDatesByTheater?theaterId={location.value['code']}"
    res = s.get(url)
    data = res.json()
    new_date = [new_date for new_date in data if date in new_date]
    if not new_date:
        print("NO DATE FOUND")
        return None
    return new_date[0]


def remove_redundant_from_name(name: str):
    return name.replace("-מדובב", "").replace("-אנגלית", "").replace("-עברית", "").replace("מדובב לעברית", "").replace(
        "אנגלית", "").strip()


def get_by_location(location: Locations, date: str, s: requests.Session):
    print("STARTED CINEMA CITY ", location.name)
    new_date = get_date(location, date, s)
    if not new_date:
        return
    url = f"https://www.cinema-city.co.il/tickets/Events?TheatreId={location.value['TheatreId']}&VenueTypeId={location.value['VenueTypeId']}&MovieId=0&Date={new_date}"
    res = s.get(url)
    for movie in res.json():
        movie_name = remove_redundant_from_name(movie.get("Name"))
        for show in movie.get("Dates"):
            time = show.get("Hour")
            link = f"https://tickets.cinema-city.co.il/order/{show.get('EventId')}"
            movies.append(
                Screening(date, "סינמה סיטי", location.value["name"], location.value['dis'], movie_name,
                          consts.MovieType.unknown, time, link, location.value['coords'])
            )

    print("DONE")


def get_movies(year: str, month: str, day: str, s: requests.Session):
    print("STARTED CINEMA CITY")
    date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)
    for location in Locations:
        get_by_location(location, date, s)
    print("DONE CINEMA CITY")
