import requests

import cinema_city
import hot_cinema
import lev
import rav_hen
import yes_planet
from consts import movies, headers, driver

from datetime import datetime as d

year = str(d.now().year)
month = str(d.now().month).zfill(2)
day = str(d.now().day).zfill(2)


def create_json():
    js = '{\n"time": "' + d.now().strftime("%d-%m-%Y") + '",\n"Screenings": ['
    for movie in movies:
        js += movie.json() + ",\n"
    js = js[:-2]
    js += "]\n}"

    with open("movies.json", "w", encoding='utf-8') as f:
        f.write(js)


def get_all_movies():
    s = requests.session()
    s.headers.update(headers)
    s.cookies.update({"hfSKey": "%7C%7C%7C%7C%7C%7C%7C%7C%7C1182_res%7C98163%7C"})
    yes_planet.get_movies(year, month, day)
    rav_hen.get_movies(year, month, day)

    driver.close()

    hot_cinema.get_movies(year, month, day, s)
    cinema_city.get_movies(year, month, day, s)
    lev.get_movies(year, month, day, s)

    create_json()
    print(len(movies))


def main():
    get_all_movies()


if __name__ == '__main__':
    main()
