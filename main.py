import json
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
    movies.sort(key=lambda x: (x.m_district.value[1], x.m_location, x.m_cinema, x.m_time))
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
    s.cookies.update({"hfSKey": "%7C%7C%7C%7C%7C%7C%7C%7C%7C1182_res%7C98163%7C"})

    date = d.now(pytz.timezone('ASIA/TEL_AVIV'))
    for i in range(days_to_check):
        print("\n\n\nstarted checking for:", date.strftime("%d-%m-%Y"), "\n")
        year = str(date.year)
        month = str(date.month).zfill(2)
        day = str(date.day).zfill(2)

        yes_planet.get_movies(year, month, day)
        rav_hen.get_movies(year, month, day)
        # driver.close()
        hot_cinema.get_movies(year, month, day, s)
        cinema_city.get_movies(year, month, day, s)
        lev.get_movies(year, month, day, s)
        date += timedelta(days=1)

    create_json()
    print(len(movies))


def main():
    get_all_movies()


if __name__ == '__main__':
    main()
