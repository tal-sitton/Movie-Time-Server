import abc


class MovieRater(abc.ABC):

    @abc.abstractmethod
    def rate(self, movie_name: str, release_year: int| None) -> float | None:
        pass
