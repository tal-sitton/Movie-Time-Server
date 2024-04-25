import abc

from seret.movie_info import MovieInfo


class MovieInfoFetcher(abc.ABC):

    @abc.abstractmethod
    def get_info(self, search_movie_name: str, original_movie_name: str) -> MovieInfo | None:
        pass
