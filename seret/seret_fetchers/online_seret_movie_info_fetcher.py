import requests
from bs4 import BeautifulSoup

from seret.seret_fetchers import seret_api, SeretMovieInfoFetcher
from seret.movie_info import SeretMovieInfo


class OnlineSeretMovieInfoFetcher(SeretMovieInfoFetcher):

    def __init__(self, session: requests.Session):
        self.session = session

    def get_from_url(self, url: str) -> SeretMovieInfo | None:
        res = self.session.get(url)
        soup = BeautifulSoup(res.content, "html.parser")
        canonical_url = seret_api.find_canonical_url(soup)
        if canonical_url != url:
            return self.get_from_url(canonical_url)
        return seret_api.get_seret_movie_info(soup)
