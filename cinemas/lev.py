import logging
from enum import Enum

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from models import Districts, MovieType, LanguageType
from models import Screening
from proxy import ProxifiedSession


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


def find_type(attributes: list | None) -> MovieType | None:
    if not attributes:
        return MovieType.unknown
    if "3D" in attributes:
        return MovieType.m_3D
    if "EVENT" in attributes:
        return None
    return MovieType.unknown


logger = logging.getLogger(__name__)


def find_dubbed(movie_info: dict) -> LanguageType:
    if movie_info['dubbedLanguage'] == 2:
        return LanguageType.DUBBED
    elif movie_info['subbedLanguage'] == 2:
        return LanguageType.SUBBED
    return LanguageType.UNKNOWN


def get_by_location(location: Locations, date: str, format_date: str, s: requests.Session) -> list[Screening]:
    logger.info(f"STARTED LEV {location.name}")
    screenings: list[Screening] = []

    url = f"https://ticket.lev.co.il/api/presentations?locationId={location.value['code']}&includeSynopsis=0"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    res = s.get(url, verify=False)
    for movie in res.json()['presentations']:
        if date not in movie['dateTime']:
            continue
        name = movie['featureName']
        time = movie['dateTime'].split(" ")[1]
        link = f"https://ticket.lev.co.il/order/{movie['id']}"
        movie_type = find_type(movie.get('featureAttributes'))
        english_name = movie.get('featureAdditionalName')
        dubbed = find_dubbed(movie)
        if movie_type is None:
            continue

        screenings.append(
            Screening(format_date, "לב", location.value["name"], location.value['dis'], name, english_name,
                      movie_type, time, link, location.value['coords'], dubbed)
        )
    logger.info(f"DONE LEV {location.name}")
    return screenings


def get_screenings(year: str, month: str, day: str, s: requests.Session) -> list[Screening]:
    logger.info("STARTED LEV")
    screenings: list[Screening] = []
    date = "{}-{}-{}".format(year, month.zfill(2), day.zfill(2))
    format_date = "{}-{}-{}".format(day.zfill(2), month.zfill(2), year)

    with ProxifiedSession(s) as ps:
        for location in Locations:
            screenings.extend(get_by_location(location, date, format_date, ps))
    logger.info("DONE LEV")
    return screenings
