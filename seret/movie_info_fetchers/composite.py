import logging
from functools import lru_cache

import requests

from consts import LOGGING_LEVEL
from seret.movie_info import MovieInfo
from seret.movie_info_fetchers import MovieInfoFetcher, ElasticMovieInfoFetcher
from seret.movie_info_fetchers.search_engines_api import search_callable
from seret.movie_raters.movie_rater import MovieRater
from seret.seret_fetchers import SeretMovieInfoFetcher


class CompositeMovieInfoFetcher(MovieInfoFetcher):

    def __init__(self, search_engine: search_callable, seret_fetcher: SeretMovieInfoFetcher, movie_rater: MovieRater,
                 session: requests.Session):
        self.seret_fetcher = seret_fetcher
        self.session = session
        self.movie_rater = movie_rater
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(LOGGING_LEVEL)

        self.fetchers = [
            ElasticMovieInfoFetcher(movie_rater),
            # SearchEngineMovieInfoFetcher(search_engine, seret_fetcher, movie_rater, session)
        ]

    @lru_cache(maxsize=None)
    def get_info(self, search_movie_name: str, original_movie_name: str) -> tuple[(MovieInfo | None), float]:
        for fetcher in self.fetchers:
            try:
                info = fetcher.get_info(search_movie_name, original_movie_name)
            except Exception as e:
                self.logger.error(f"Failed to get info for {search_movie_name} using {fetcher.__class__.__name__}: {e}")
                continue
            if info:
                self.logger.info(f"Got info for {search_movie_name} using {fetcher.__class__.__name__}")
                return info
        self.logger.warning(f"Failed to get info for {search_movie_name}")
        return None, 0
