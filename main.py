import json
import logging
import pathlib
from datetime import datetime, timedelta

import pytz
import requests

import cinema_city
import consts
import hot_cinema
import lev
import movieland
import rav_hen
import yes_planet
from consts import screenings, headers
from seret.seret_movie_info import get_movies_info

days_to_check = 5


def create_json():
    screenings.sort(key=lambda x: (x.m_district.value[1], x.m_location, x.m_cinema, x.m_date, x.m_time))
    js = json.dumps({
        "time": datetime.now().strftime("%d-%m-%Y"),
        "Movies": [movie.to_dict() for movie in consts.movies],
        "Screenings": [screening.to_dict() for screening in screenings]
    })

    # with open("movies.json", "w", encoding='utf-8') as f:
    #     f.write(json.dumps(json.loads(js), indent=2))

    # USE FOR DEBUGGING
    with open("movies.json", "wb") as f:
        f.write(json.dumps(json.loads(js), indent=2, ensure_ascii=False).encode("utf-8"))


def get_all_screenings():
    s = requests.session()
    s.headers.update(headers)

    date = datetime.now(pytz.timezone('ASIA/TEL_AVIV'))
    for i in range(days_to_check):
        print("\n\n\nstarted checking for:", date.strftime("%d-%m-%Y"), "\n")
        year = str(date.year)
        month = str(date.month).zfill(2)
        day = str(date.day).zfill(2)

        try:
            yes_planet.get_screenings(year, month, day, s)
        except Exception as e:
            logging.error('Yes Planet crashed!', exc_info=e)
        try:
            rav_hen.get_screenings(year, month, day, s)
        except Exception as e:
            logging.error('Rav Hen crashed!', exc_info=e)
        try:
            hot_cinema.get_screenings(year, month, day, s)
        except Exception as e:
            logging.error('Hot Cinema crashed!', exc_info=e)

        try:
            cinema_city.get_screenings(year, month, day, s)
        except Exception as e:
            logging.error('Cinema city crashed!', exc_info=e)

        try:
            lev.get_screenings(year, month, day, s)
        except Exception as e:
            logging.error('Lev crashed!', exc_info=e)

        try:
            movieland.get_screenings(year, month, day, s)
        except Exception as e:
            logging.error('MovieLand crashed!', exc_info=e)

        date += timedelta(days=1)

    consts.movies = get_movies_info(s, screenings)
    create_json()
    print(len(screenings))


def prepare_logs(logs_path):
    if logs_path.exists():
        logs_path.unlink()

    file_handler = logging.FileHandler('logs.txt', delay=True)
    file_handler.setLevel(logging.DEBUG)
    logging.root.addHandler(file_handler)


def main():
    logs_path = pathlib.Path('logs.txt')
    prepare_logs(logs_path)
    get_all_screenings()


if __name__ == '__main__':
    main()
