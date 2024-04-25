import requests

from seret.movie_raters import imdb_api, MovieRater


class IMDBMovieRater(MovieRater):
    def __init__(self, session: requests.Session):
        self.session = session

    def rate(self, movie_name: str, release_year: int | None) -> float | None:
        return imdb_api.get_imdb_rating(self.session, movie_name, release_year)
