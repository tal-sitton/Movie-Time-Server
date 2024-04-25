import os
from enum import Enum

ELASTIC_HOST: str = os.environ.get("ELASTIC_HOST") or "http://localhost:9200"

ELASTIC_MOVIES_INDEX = "seret_movies"

ELASTIC_NEEDED_SEARCH_MIN_SCORE = 8


class ElasticSearchField(Enum):
    NAME = "name"
    ENGLISH_NAME = "english_name"
    URL = "url"
