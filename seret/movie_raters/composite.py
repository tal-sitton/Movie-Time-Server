import logging

import requests

from seret.movie_raters import MovieRater, IMDBMovieRater


class CompositeMovieRater(MovieRater):
    def __init__(self, session: requests.Session):
        self.session = session

        self.raters = [
            IMDBMovieRater(self.session),
        ]

    def rate(self, movie_name: str, release_year: int | None) -> float | None:
        for rater in self.raters:
            rating = rater.rate(movie_name, release_year)
            if rating:
                return rating
        logging.getLogger(__name__).warning(f"Failed to get rating for {movie_name}")
        return None
