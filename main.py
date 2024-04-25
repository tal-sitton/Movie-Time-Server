import json
import logging
import pathlib
from datetime import datetime, timedelta
from typing import List

import pytz
import requests
import retry

import consts
from models import Screening
from consts import headers
from models import cinemas_get_screenings, GetScreeningCallable
from seret.info_fetcher import fetch_movies_info
from seret.seret_api import MovieInfo

days_to_check = 5


def create_json(screenings: List[Screening], movies: List[MovieInfo]):
    screenings.sort(key=lambda x: (x.m_district.value[1], x.m_location, x.m_cinema, x.m_date, x.m_time))
    js = json.dumps({
        "time": datetime.now().strftime("%d-%m-%Y"),
        "Movies": [movie.to_dict() for movie in movies],
        "Screenings": [screening.to_dict() for screening in screenings]
    })

    with open("movies.json", "wb") as f:
        f.write(json.dumps(json.loads(js), indent=2, ensure_ascii=False).encode("utf-8"))


def get_all_screenings():
    s = requests.Session()
    s.headers.update(headers)
    screenings: List[Screening] = []

    date = datetime.now(pytz.timezone('ASIA/TEL_AVIV'))
    for i in range(days_to_check):
        logging.info("*" * 20)
        logging.info("started checking for:" + date.strftime("%d-%m-%Y"))

        for cinema, get_screening in cinemas_get_screenings.items():
            screenings.extend(get_screenings_from_cinema(get_screening, cinema, date, s))

        date += timedelta(days=1)

    movies = fetch_movies_info(s, screenings)
    create_json(screenings, movies)
    logging.info(len(screenings))


def get_screenings_from_cinema(get_screening: GetScreeningCallable, cinema: str, date: datetime, s: requests.Session) \
        -> List[Screening]:
    try:
        return unsafe_get_screenings_from_cinema(get_screening, cinema, date, s)
    except AssertionError as e:
        logging.error(f'{cinema} crashed: {e}')
    except Exception as e:
        logging.exception(f'{cinema} crashed', exc_info=e)
    return []


@retry.retry(exceptions=AssertionError, tries=3, delay=1, backoff=2)
def unsafe_get_screenings_from_cinema(get_screening: GetScreeningCallable, cinema: str, date: datetime,
                                      s: requests.Session) -> List[Screening]:
    year = str(date.year)
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)

    screenings = get_screening(year, month, day, s)
    if not screenings:
        raise AssertionError(f'{cinema} returned empty list')
    return get_screening(year, month, day, s)


def mute_other_loggers():
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.getLogger('elastic_transport').setLevel(logging.ERROR)


def prepare_logs(logs_path: pathlib.Path):
    logging.basicConfig(level=consts.LOGGING_LEVEL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        encoding='utf-8')
    if logs_path.exists():
        logs_path.unlink()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler('logs.txt', encoding='utf-8', delay=True)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(consts.LOGGING_LEVEL)
    logging.root.addHandler(file_handler)

    mute_other_loggers()


def main():
    logs_path = pathlib.Path('logs.txt')
    prepare_logs(logs_path)
    get_all_screenings()


if __name__ == '__main__':
    main()
