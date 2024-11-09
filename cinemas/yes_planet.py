import logging
from datetime import datetime
from enum import Enum

import requests

from models import MovieType, Districts, LanguageType
from models import Screening


class Locations(Enum):
    """
    locations and codes
    """
    RISHON = {
        "code": "1072",
        "name": "ראשון לציון",
        "dis": Districts.DAN,
        "coords": (31.9798, 34.7475),
    }
    AYALON = {
        "code": "1025",
        "name": "קניון אילון",
        "dis": Districts.DAN,
        "coords": (32.0995, 34.8272),
    }
    ZICHRON = {
        "code": "1075",
        "name": "זכרון יעקב",
        "dis": Districts.ZAFON,
        "coords": (32.5697, 34.9333),
    }
    HAIFA = {
        "code": "1070",
        "name": "חיפה",
        "dis": Districts.ZAFON,
        "coords": (32.7937, 35.0383),
    }
    JERUSALEM = {
        "code": "1073",
        "name": "ירושלים",
        "dis": Districts.JERUSALEM,
        "coords": (31.7624, 35.2257),
    }
    BEER_SHEVA = {
        "code": "1074",
        "name": "באר שבע",
        "dis": Districts.DAROM,
        "coords": (31.2244, 34.8010),
    }


def find_type(movie_type: list):
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


def find_dubbed(movie_info: list) -> LanguageType:
    if "DUB" in movie_info:
        return LanguageType.DUBBED
    elif "SUBTITLE" in movie_info:
        return LanguageType.SUBBED
    return LanguageType.UNKNOWN


all_movies: dict[int, tuple[str, str]] = {}
all_screenings: dict[str, dict[str, list[Screening]]] = {}

logger = logging.getLogger(__name__)


def login(s: requests.Session) -> str:
    res = s.post("https://pub-api.biggerpicture.ai/mapiAPI/login",
                 json={"accessCode": "YP", "password": "MAPI132", "username": "MAPI1"})
    return res.json().get("token")


def get_all_movies(s: requests.Session, token: str) -> dict[int, tuple[str, str]]:
    headers = {"Authorization": f"Bearer {token}"}
    res = s.get("https://pub-api.biggerpicture.ai/mapiAPI/group/eventMasters?full=true", headers=headers)
    raw_movies = res.json().get("eventMasters")
    movies = {}
    for movie in raw_movies:
        edi = movie.get("edi")
        heb_title = next((name['value'] for name in movie.get('webNameInLanguage') if name['key'] == 'he-IL'), None)
        original_title = movie.get("originalName") if movie.get("originalName") != heb_title else next(
            (name['value'] for name in movie.get('webNameInLanguage') if name['key'] != 'he-IL'), None)
        movies[edi] = (heb_title, original_title)
    return movies


def get_all_screenings(s: requests.Session, token: str) -> dict[str, dict[str, list[Screening]]]:
    screenings: dict[str, dict[str, list[Screening]]] = {}

    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://pub-api.biggerpicture.ai/mapiAPI/group/events?key=MAPI&territory=il&group=true{''.join(['&siteId=' + cinema.value.get('code') for cinema in Locations])}"
    res = s.get(url, headers=headers)

    for raw_screening in res.json().get("events"):
        parsed_date = datetime.fromisoformat(raw_screening.get("dtf"))
        screening_date = parsed_date.strftime("%d-%m-%Y")
        raw_location = str(raw_screening.get("sId"))
        if screening_date not in screenings:
            screenings[screening_date] = {}
        if raw_location not in screenings[screening_date]:
            screenings[screening_date][raw_location] = []

        screening_time = parsed_date.strftime("%H:%M")
        screening_location = [location.value for location in Locations if location.value.get('code') == raw_location][0]
        title, eng_title = all_movies.get(raw_screening.get("edi"))
        link = f"https://tickets3.planetcinema.co.il/site/{raw_location}?code={raw_screening.get('eventCode')}&saleChannelCode=web"

        screening = Screening(screening_date, "יס פלאנט", screening_location['name'], screening_location['dis'], title,
                              eng_title, find_type(raw_screening.get("attrs")), screening_time, link,
                              screening_location['coords'], find_dubbed(raw_screening.get("attrs")))
        screenings[screening_date][raw_location].append(screening)
    return screenings


def init_data(s: requests.Session):
    global all_movies, all_screenings
    if not all_movies or not all_screenings:
        logger.info("STARTED YES PLANET INIT")
        token = login(s)
        all_movies = get_all_movies(s, token)
        all_screenings = get_all_screenings(s, token)


def get_by_location(location: Locations, format_date: str, s: requests.Session) -> list[Screening]:
    logger.info(f"STARTED YES PLANET {location.name}")
    init_data(s)
    screenings: list[Screening] = all_screenings.get(format_date, {}).get(location.value['code'], [])
    logger.info(f"DONE YES PLANET {location.name}")
    return screenings


def get_screenings(year: str, month: str, day: str, s: requests.Session) -> list[Screening]:
    logger.info("STARTED YES PLANET")
    screenings: list[Screening] = []
    format_date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)

    for location in Locations:
        try:
            screenings.extend(get_by_location(location, format_date, s))
        except Exception as e:
            logger.exception(f"Failed to get screenings for {location.name}", exc_info=e)

    logger.info("DONE YES PLANET")
    return screenings


if __name__ == '__main__':
    s = requests.Session()
    print(get_screenings(str(datetime.now().year), str(datetime.now().month).zfill(2),
                         str(datetime.now().day + 1).zfill(2), s))
