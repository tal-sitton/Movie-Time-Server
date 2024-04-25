from typing import Callable, Optional, Type

import requests

from seret.movie_info_fetchers.search_engines_api import ScoredSearchResult

search_callable: Type = Callable[
    [str, Optional[str], Optional[str], Optional[str], requests.Session], list[ScoredSearchResult]
]
