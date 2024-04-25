from seret import ElasticSearchField, elastic_utils
from seret.movie_info import SeretMovieInfo
from seret.seret_fetchers import SeretMovieInfoFetcher


class ElasticSeretMovieInfoFetcher(SeretMovieInfoFetcher):

    def get_from_url(self, url: str) -> SeretMovieInfo | None:
        return elastic_utils.search(url, ElasticSearchField.URL)
