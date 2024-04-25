import logging

import requests

from seret.movie_info import SeretMovieInfo
from seret.seret_fetchers import SeretMovieInfoFetcher, OnlineSeretMovieInfoFetcher, ElasticSeretMovieInfoFetcher


class CompositeSeretMovieInfoFetcher(SeretMovieInfoFetcher):

    def __init__(self, session: requests.Session):
        self.session = session
        self.fetchers = [
            ElasticSeretMovieInfoFetcher(),
            OnlineSeretMovieInfoFetcher(session)
        ]

    def get_from_url(self, url: str) -> SeretMovieInfo | None:
        for fetcher in self.fetchers:
            movie_info = fetcher.get_from_url(url)
            if movie_info:
                return movie_info
        logging.getLogger(__name__).warning(f"Failed to get seret info from {url}")
        return None
