import json
import logging
import os
import pathlib
from datetime import datetime as d, timedelta

import pytz
import requests

import cinema_city
import hot_cinema
import lev
import rav_hen
import yes_planet
from consts import movies, headers

days_to_check = 5


def create_json():
    movies.sort(key=lambda x: (x.m_district.value[1], x.m_location, x.m_cinema, x.m_date, x.m_time))
    js = '{\n"time": "' + d.now().strftime("%d-%m-%Y") + '",\n"Screenings": ['
    for movie in movies:
        js += movie.json() + ",\n"
    js = js[:-2]
    js += "]\n}"

    with open("movies.json", "w", encoding='utf-8') as f:
        f.write(json.dumps(json.loads(js), indent=2))


def get_all_movies():
    s = requests.session()
    s.headers.update(headers)

    date = d.now(pytz.timezone('ASIA/TEL_AVIV'))
    for i in range(days_to_check):
        print("\n\n\nstarted checking for:", date.strftime("%d-%m-%Y"), "\n")
        year = str(date.year)
        month = str(date.month).zfill(2)
        day = str(date.day).zfill(2)

        try:
            yes_planet.get_movies(year, month, day, s)
        except Exception as e:
            logging.error('Yes Planet crashed!', exc_info=e)
        try:
            rav_hen.get_movies(year, month, day, s)
        except Exception as e:
            logging.error('Rav Hen crashed!', exc_info=e)
        try:
            hot_cinema.get_movies(year, month, day, s)
        except Exception as e:
            logging.error('Hot Cinema crashed!', exc_info=e)

        try:
            cinema_city.get_movies(year, month, day, s)
        except Exception as e:
            logging.error('Cinema city crashed!', exc_info=e)

        try:
            lev.get_movies(year, month, day, s)
        except Exception as e:
            logging.error('Lev crashed!', exc_info=e)
        date += timedelta(days=1)
        break

    create_json()
    print(len(movies))


def prepare_logs(logs_path):
    if logs_path.exists():
        logs_path.unlink()

    file_handler = logging.FileHandler('logs.txt', delay=True)
    file_handler.setLevel(logging.DEBUG)
    logging.root.addHandler(file_handler)


def main():
    logs_path = pathlib.Path('logs.txt')
    prepare_logs(logs_path)
    get_all_movies()


if __name__ == '__main__':
    main()
