import logging

import requests

from models import Screening
from seret.movie_info import MovieInfo, DEFAULT_DESCRIPTION
from seret.movie_info_fetchers import MovieInfoFetcher, CompositeMovieInfoFetcher
from seret.movie_info_fetchers.search_engines_api import composite_search
from seret.movie_raters import CompositeMovieRater
from seret.seret_fetchers import CompositeSeretMovieInfoFetcher


def create_movie_info_fetcher(session: requests.Session) -> MovieInfoFetcher:
    seret_fetcher = CompositeSeretMovieInfoFetcher(session)
    movie_rater = CompositeMovieRater(session)
    search_engine = composite_search
    return CompositeMovieInfoFetcher(search_engine, seret_fetcher, movie_rater, session)


def fetch_info(fetcher: MovieInfoFetcher, search_movie_name: str, original_movie_name: str) -> MovieInfo:
    info: MovieInfo = None
    if search_movie_name:
        info = fetcher.get_info(search_movie_name, original_movie_name)
    if not info:
        info = fetcher.get_info(original_movie_name, original_movie_name)
    if not info:
        info = MovieInfo(original_movie_name, None, DEFAULT_DESCRIPTION, None, "")
    return info


def fetch_movies_info(session: requests.Session, screenings: list[Screening]) -> list[MovieInfo]:
    fetcher = create_movie_info_fetcher(session)
    movies: dict[str, MovieInfo] = {}
    failed = []
    for screening in screenings:
        info = fetch_info(fetcher, screening.m_eng_title, screening.m_title)
        if not movies.get(info.name):
            movies[info.name] = info

            if info.description == DEFAULT_DESCRIPTION:
                logging.getLogger(__name__).error(
                    f"Failed to get info for {screening.m_eng_title} and {screening.m_title}")
                failed.append(screening)

        screening.m_title = info.name
        if info.english_name:
            screening.m_eng_title = info.english_name

    logging.getLogger(__name__).error(f"Failed to get info for {len(failed)} movies: {[f.to_dict() for f in failed]}")
    return list(movies.values())
