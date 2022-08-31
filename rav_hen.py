import time
from enum import Enum

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Screening import Screening
from consts import driver, movies, MovieType, Districts


class Locations(Enum):
    """
    locations and codes
    """
    GIVATAIM = {
        "code": "1058",
        "name": "גבעתיים",
        "dis": Districts.DAN,
    }
    DIZINGOF = {
        "code": "1071",
        "name": "דיזינגוף",
        "dis": Districts.DAN,
    }
    MODIIN = {
        "code": "1069",
        "name": "מודיעין",
        "dis": Districts.JERUSALEM,
    }
    KIRYAT_ONO = {
        "code": "1062",
        "name": "קריית אונו",
        "dis": Districts.DAN,
    }


def prepare(location: Locations, date: str):
    url = f"https://www.rav-hen.co.il/#/buy-tickets-by-cinema?in-cinema={location.value['code']}&at={date}&view-mode=list"
    driver.get(url)
    driver.refresh()
    time.sleep(1)
    if driver.current_url != url:
        print("NO DATE FOUND")
        return []
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'qb-movie-name')))
    return driver.find_elements(By.CLASS_NAME, "qb-movie")


def get_by_location(location: Locations, date: str, format_date: str):
    print("STARTED RAV HEN ", location.name)
    movies_data = prepare(location, date)
    for movie in movies_data:
        movie_name = movie.find_element(By.CLASS_NAME, "qb-movie-name").text.replace("עם כתוביות", "").replace("עברית",
                                                                                                               "").strip()
        all_data = movie.find_elements(By.CLASS_NAME, "qb-movie-info-column")
        for type_data in all_data:
            data = type_data.text
            for info in type_data.find_elements(By.TAG_NAME, "a"):
                link = info.get_attribute("data-url")
                m_time = info.text
                movies.append(
                    Screening(format_date, "רב חן", location.value['name'], location.value['dis'], movie_name,
                              MovieType.m_2D, m_time, link)
                )
    print("DONE")


def get_movies(year: str, month: str, day: str):
    print("STARTED RAV HEN")
    date = "{}-{}-{}".format(year, month.zfill(2), day.zfill(2))
    format_date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)
    for location in Locations:
        get_by_location(location, date, format_date)
    print("DONE RAV HEN")
