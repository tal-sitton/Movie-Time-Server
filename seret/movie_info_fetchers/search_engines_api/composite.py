import logging
from typing import Optional

import requests
from search_engine_parser.core.exceptions import NoResultsOrTrafficError

from seret.movie_info_fetchers.search_engines_api import ScoredSearchResult, google_search, bing_search, \
    search_callable, duck_search

engines_scores: dict[search_callable, tuple[str, float]] = {
    google_search: ("google", 1),
    bing_search: ("bing", 0.8),
    duck_search: ("duckduckgo", 0.6),
}


def search(query: str, wanted_term: Optional[str] = None, remove_regex: Optional[str] = None,
           need_in_url: Optional[str] = None, session: requests.Session = requests.Session()) \
        -> list[ScoredSearchResult]:
    for engine_search, engine_info in engines_scores.items():
        engine_name, score_multiplier = engine_info
        try:
            results = engine_search(query, wanted_term, remove_regex, need_in_url, session)
            for result in results:
                result.score *= score_multiplier
            if results:
                return results
        except NoResultsOrTrafficError as e:
            logging.getLogger(__name__).warning(f"Failed to search with {engine_name}: {e}")
        except Exception as e:
            logging.getLogger(__name__).exception(f"Failed to search with {engine_name}", exc_info=e)
    return []
