from enum import Enum

import requests

import consts
from Screening import Screening
from consts import movies


class Locations(Enum):
    """
    locations and codes
    """
    GLILOT = {
        "code": "1",
        "TheatreId": "1170",
        "VenueTypeId": "1",
        "name": "גלילות"
    }
    RISHON = {
        "code": "2",
        "TheatreId": "1173",
        "VenueTypeId": "1",
        "name": "ראשון לציון"
    }
    JERUSALEM = {
        "code": "3",
        "TheatreId": "1174",
        "VenueTypeId": "1",
        "name": "ירושלים"
    }
    KFAR_SABBA = {
        "code": "4",
        "TheatreId": "1175",
        "VenueTypeId": "1",
        "name": "כפר סבא"
    }
    NATANIA = {
        "code": "5",
        "TheatreId": "1176",
        "VenueTypeId": "1",
        "name": "נתניה"
    }
    BEER_SHEVA = {
        "code": "17",
        "TheatreId": "1178",
        "VenueTypeId": "1",
        "name": "באר שבע"
    }
    HADERA = {
        "code": "13",
        "TheatreId": "1350",
        "VenueTypeId": "1",
        "name": "חדרה"
    }
    ASHDOD = {
        "code": "25",
        "TheatreId": "1181",
        "VenueTypeId": "1",
        "name": "אשדוד"
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


def get_by_location(location: Locations, date: str, s: requests.Session):
    print("STARTED CINEMA CITY ", location.name)
    new_date = get_date(location, date, s)
    if not new_date:
        return
    url = f"https://www.cinema-city.co.il/tickets/Events?TheatreId={location.value['TheatreId']}&VenueTypeId={location.value['VenueTypeId']}&MovieId=0&Date={new_date}"
    res = s.get(url)
    for movie in res.json():
        movie_name = movie.get("Name").replace("-מדובב", "").replace("-אנגלית", "").replace("-עברית", "").strip()
        for show in movie.get("Dates"):
            time = show.get("Hour")
            link = f"https://tickets.cinema-city.co.il/order/{show.get('EventId')}"
            movies.append(
                Screening(date, "Cinema City", location.value["name"], movie_name, consts.MovieType.m_2D, time, link))

    print("DONE")


def get_movies(year: str, month: str, day: str, s: requests.Session):
    print("STARTED CINEMA CITY")
    date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)
    for location in Locations:
        get_by_location(location, date, s)
    print("DONE CINEMA CITY")
