from typing import Optional

import requests
from search_engine_parser.core.engines.duckduckgo import Search as DuckSearch

from seret.movie_info_fetchers.search_engines_api.base_search_api import handle_results
from seret.movie_info_fetchers.search_engines_api.search_result import ScoredSearchResult

_engine = DuckSearch()


def search(query: str, wanted_term: Optional[str] = None, remove_regex: Optional[str] = None,
           need_in_url: Optional[str] = None, session: requests.Session = requests.Session()) \
        -> list[ScoredSearchResult]:
    headers = _engine.headers()

    if need_in_url:
        query += f" inurl:{need_in_url}"

    url = f"https://duckduckgo.com/?q={query}"

    res = session.get(url, headers=headers)

    return handle_results(res, _engine, wanted_term, remove_regex)


if __name__ == '__main__':
    print(
        search("Forever Young site:seret.co.il", "צעירים לנצח", need_in_url="movies/s_movies.asp?MID="))
