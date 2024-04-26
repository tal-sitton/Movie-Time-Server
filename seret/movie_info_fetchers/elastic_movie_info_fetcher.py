from seret import elastic_utils, ElasticSearchField, ELASTIC_NEEDED_SEARCH_MIN_SCORE
from seret.movie_info import MovieInfo
from seret.movie_info_fetchers import MovieInfoFetcher
from seret.movie_raters import MovieRater


class ElasticMovieInfoFetcher(MovieInfoFetcher):

    def __init__(self, movie_rater: MovieRater):
        self.movie_rater = movie_rater

    def get_info(self, search_movie_name: str, original_movie_name: str) -> MovieInfo | None:
        if search_movie_name == original_movie_name:
            search_field = ElasticSearchField.NAME
        else:
            search_field = ElasticSearchField.ENGLISH_NAME
        partial_info = elastic_utils.search(search_movie_name, search_field, ELASTIC_NEEDED_SEARCH_MIN_SCORE)
        if not partial_info:
            return None

        rating = self.movie_rater.rate(partial_info.english_name, partial_info.release_year)
        if not rating:
            rating = self.movie_rater.rate(partial_info.name, partial_info.release_year)

        return MovieInfo(partial_info.name, partial_info.english_name, partial_info.description, rating,
                         partial_info.image_url)
