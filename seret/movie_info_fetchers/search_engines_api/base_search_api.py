import difflib
import re
from typing import List, Optional

from bs4 import BeautifulSoup
from requests import Response
from search_engine_parser.core.base import SearchResult, BaseSearch

from seret.movie_info_fetchers.search_engines_api.search_result import ScoredSearchResult, ParsedSearchResult

DIFF_SCORE_WEIGHT = 0.4
POSITION_SCORE_WEIGHT = 1 - DIFF_SCORE_WEIGHT

MIN_DIFF_SCORE = 0.65  # 0 to 1
MIN_DIFF_SCORE_CALC = MIN_DIFF_SCORE * DIFF_SCORE_WEIGHT


def base_parse_results(results: list[dict]) -> list[ParsedSearchResult]:
    parsed_results: list[ParsedSearchResult] = []
    for result in results:
        if not result:
            continue
        parsed_results.append(
            ParsedSearchResult(title=result['titles'], url=result['links'], description=result['descriptions']))
    return parsed_results


def _score(results: list[ParsedSearchResult], wanted_term: str) -> list[ScoredSearchResult]:
    """
    Score the results based on difference between the title and the wanted term
    """
    scored_results: List[ScoredSearchResult] = []

    for i, result in enumerate(results, 1):
        diff_score = difflib.SequenceMatcher(None, result.title, wanted_term).ratio() * DIFF_SCORE_WEIGHT
        if diff_score < MIN_DIFF_SCORE_CALC:
            continue

        position_score = (len(results) - i) / (len(results) - 1) * POSITION_SCORE_WEIGHT if len(
            results) > 1 else POSITION_SCORE_WEIGHT

        score = diff_score + position_score

        scored_results.append(result.score(score))
    return scored_results


def handle_results(res: Response, engine: BaseSearch, wanted_term: Optional[str] = None,
                   remove_regex: Optional[str] = None) -> list[ScoredSearchResult]:
    soup = BeautifulSoup(res.content, "html.parser")

    search_results: SearchResult = engine.get_results(soup)
    raw_results: list[dict] = search_results.results

    results = base_parse_results(raw_results)

    if remove_regex:
        for result in results:
            result.title = re.sub(remove_regex, "", result.title, re.I)

    if wanted_term:
        scored_results = _score(results, wanted_term)
    else:
        scored_results: list[ScoredSearchResult] = []
        if len(results) == 1:
            scored_results.append(results[0].score(10))
        else:
            for i, result in enumerate(results, 1):
                score = (len(results) - i) / (len(results) - 1) * 10
                scored_results.append(result.score(score))

    return sorted(scored_results, key=lambda x: x.score, reverse=True)
