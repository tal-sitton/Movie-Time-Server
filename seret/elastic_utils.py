from elasticsearch import Elasticsearch

from seret import ELASTIC_HOST, ELASTIC_MOVIES_INDEX, ElasticSearchField
from seret.movie_info import SeretMovieInfo


def search(search_term: str, search_field: ElasticSearchField, min_needed_score: int = 0,
           fuzzy=False) -> SeretMovieInfo | None:
    with Elasticsearch(hosts=[ELASTIC_HOST]) as client:
        if fuzzy:
            body = {"query": {"bool": {
                "should": [{"match": {search_field.value: {"query": search_term, "fuzziness": "AUTO"}}}, {
                    "match": {search_field.value: {"query": search_term.replace('"', ""), "fuzziness": "AUTO"}}}]}}}
        else:
            body = {"query": {"match": {search_field.value: search_term}}}
        res = client.search(index=ELASTIC_MOVIES_INDEX, body=body)
    raw_hits = res.body.get('hits')
    max_score = raw_hits.get('max_score')

    if not raw_hits or not raw_hits.get('hits'):
        return None

    hits = raw_hits.get('hits')

    if len(hits) > 2:
        difference_in_score = hits[0].get('_score') - hits[1].get('_score')
    else:
        difference_in_score = 99

    if not max_score or max_score < min_needed_score or difference_in_score < 0.65:
        return None

    wanted_result: dict = hits[0].get('_source')
    return SeretMovieInfo(wanted_result.get('english_name'), wanted_result.get('name'),
                          wanted_result.get('description'), wanted_result.get('image_url'), wanted_result.get('year'))
