import abc

from seret.movie_info import SeretMovieInfo


class SeretMovieInfoFetcher(abc.ABC):

    @abc.abstractmethod
    def get_from_url(self, url: str) -> SeretMovieInfo | None:
        pass
