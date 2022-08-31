import time
from enum import Enum

from selenium.webdriver.common.by import By

from Screening import Screening
from consts import driver, MovieType, movies, Districts


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


def find_type(movie_type: str):
    if "4DX" in movie_type:
        return MovieType.m_4DX
    if "VIP" in movie_type:
        return MovieType.m_VIP
    elif "IMAX" in movie_type:
        return MovieType.m_IMAX
    elif "3D" in movie_type:
        return MovieType.m_3D
    elif "SCREENX" in movie_type:
        return MovieType.m_SCREENX
    else:
        return MovieType.m_2D


def prepare(location: Locations, date: str):
    url = f"https://www.yesplanet.co.il/#/buy-tickets-by-cinema?in-cinema={location.value['code']}&at={date}&view-mode=list"
    driver.get(url)
    driver.refresh()
    time.sleep(1)
    if driver.current_url != url:
        print("NO DATE FOUND")
        return []
    return driver.find_elements(By.CLASS_NAME, "qb-movie")


def get_by_location(location: Locations, date: str, format_date: str):
    print("STARTED YES PLANET ", location.name)
    movies_data = prepare(location, date)
    for movie in movies_data:
        movie_name = movie.find_element(By.CLASS_NAME, "qb-movie-name").text.replace("עברית עם כתוביות", "").strip()
        all_data = movie.find_elements(By.CLASS_NAME, "qb-movie-info-column")
        for type_data in all_data:
            data = type_data.text
            movie_type = data.split("\n")[0]
            movie_type = find_type(movie_type)
            for info in type_data.find_elements(By.TAG_NAME, "a"):
                link = info.get_attribute("data-url")
                if not link:
                    continue
                m_time = info.text
                movies.append(
                    Screening(format_date, "יס פלאנט", location.value['name'], location.value['dis'], movie_name,
                              movie_type, m_time, link)
                )
    print("DONE")


def get_movies(year: str, month: str, day: str):
    print("STARTED YES PLANET")
    date = "{}-{}-{}".format(year, month.zfill(2), day.zfill(2))
    format_date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)
    for location in Locations:
        get_by_location(location, date, format_date)
    print("DONE YES PLANET")
