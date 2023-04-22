from typing import List

import requests

from Screening import Screening
from . import seret_api
from .seret_api import Movie


def get_movies_info(session: requests.Session, screenings: List[Screening]) -> List[Movie]:
    movies = []
    old_titles_done = {}
    movie_titles = list(set([screening.m_title for screening in screenings]))
    checked = 1
    for screening in screenings:
        if screening.m_title in old_titles_done:
            screening.m_title = old_titles_done.get(screening.m_title)
            continue
        print(fr'{checked}\{len(movie_titles)} Getting info for {screening.m_title} ...')
        info = seret_api.get_info(session, screening.m_title)
        old_titles_done[screening.m_title] = info.name
        screening.m_title = info.name

        if not [m for m in movies if m.name == info.name]:
            movies.append(info)

        checked += 1
    return movies
