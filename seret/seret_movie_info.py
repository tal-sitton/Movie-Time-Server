from typing import List, Dict

import requests

from Screening import Screening
from . import seret_api
from .seret_api import Movie

DEFAULT_DESCRIPTION = "לא נמצא תיאור"


def get_cached_title(screening: Screening, cached_titles: Dict[str, List[str]]) -> str or None:
    for correct_title, possible_titles in cached_titles.items():
        if screening.m_eng_title:
            if screening.m_title in possible_titles or screening.m_eng_title in possible_titles:
                cached_titles[correct_title] = list({*possible_titles, screening.m_title, screening.m_eng_title})
                return correct_title
        if screening.m_title in possible_titles:
            return correct_title
    return None


def get_movies_info(session: requests.Session, screenings: List[Screening]) -> List[Movie]:
    movies = []
    old_titles_done: Dict[str, List[str]] = {}
    movie_titles = list(set([screening.m_title for screening in screenings]))
    checked = 1
    for screening in screenings:
        cached_title = get_cached_title(screening, old_titles_done)
        if cached_title:
            screening.m_title = cached_title
            continue
        print(fr'{checked}\{len(movie_titles)} Getting info for {screening.m_title} ...')
        info = None
        if screening.m_eng_title:
            info = seret_api.get_info(session, screening.m_eng_title, screening.m_title)
        if not info:
            info = seret_api.get_info(session, screening.m_title, screening.m_title)

        if not info:
            info = Movie(screening.m_title, DEFAULT_DESCRIPTION, None, "")

        if not old_titles_done.get(info.name):
            old_titles_done[info.name] = []

        if screening.m_eng_title:
            old_titles_done[info.name] = list({*old_titles_done[info.name], screening.m_title, screening.m_eng_title})
        else:
            old_titles_done[info.name] = list({*old_titles_done[info.name], screening.m_title})

        screening.m_title = info.name

        if not [m for m in movies if m.name == info.name]:
            movies.append(info)

        checked += 1
    return movies
