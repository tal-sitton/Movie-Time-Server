import requests

from seret.movie_info import MovieInfo
from seret.movie_info_fetchers import MovieInfoFetcher
from seret.movie_info_fetchers.search_engines_api import search_callable
from seret.movie_raters import MovieRater
from seret.seret_fetchers import SeretMovieInfoFetcher


class SearchEngineMovieInfoFetcher(MovieInfoFetcher):

    def __init__(self, search_engine: search_callable, seret_fetcher: SeretMovieInfoFetcher, movie_rater: MovieRater,
                 session: requests.Session):
        self.search_engine = search_engine
        self.seret_fetcher = seret_fetcher
        self.session = session
        self.movie_rater = movie_rater

    def get_info(self, search_movie_name: str, original_movie_name: str) -> MovieInfo | None:
        query = f"{search_movie_name} site:seret.co.il"
        needed_in_url = "movies/s_movies.asp?MID="
        remove_regex = r"Seret.co.il|סרט ::| :: |אתר סרט|\||<b>|</b>"
        results = self.search_engine(query, original_movie_name, remove_regex, needed_in_url, self.session)
        if not results or results[0].score < 0.4:
            return None

        url = results[0].url
        partial_info = self.seret_fetcher.get_from_url(url)
        if not partial_info:
            return None
        rating = self.movie_rater.rate(partial_info.english_name, partial_info.release_year)
        if not rating:
            rating = self.movie_rater.rate(partial_info.name, partial_info.release_year)

        return MovieInfo(partial_info.name, partial_info.english_name, partial_info.description, rating,
                         partial_info.image_url)
