import dataclasses

DEFAULT_DESCRIPTION = "לא נמצא תיאור"


@dataclasses.dataclass
class SeretMovieInfo:
    english_name: str
    name: str
    description: str
    image_url: str
    release_year: int | None


@dataclasses.dataclass
class MovieInfo:
    name: str
    description: str
    rating: float | None
    image_url: str

    def to_dict(self) -> dict:
        return self.__dict__
