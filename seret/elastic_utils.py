from datetime import timedelta, datetime

from elasticsearch import Elasticsearch

from seret import ELASTIC_HOST, ELASTIC_MOVIES_INDEX, ElasticSearchField
from seret.movie_info import SeretMovieInfo


def search(search_term: str, search_field: ElasticSearchField, min_needed_score: int = 0,
           fuzzy=False) -> tuple[(SeretMovieInfo | None), float]:
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
        return None, 0

    hits = raw_hits.get('hits')

    hits = [hit for hit in hits if not hit.get('_source').get('premiere') or
            datetime.fromisoformat(hit.get('_source').get('premiere')) - datetime.now() < timedelta(days=7)]

    same_score_hits = [hit for hit in hits if hit.get('_score') == hits[0].get('_score')]
    same_source_hits = [hit for hit in hits if hits[0].get("_id").isdigit() == hit.get("_id").isdigit()]

    if len(same_score_hits) >= 4:
        difference_in_score = 0
    elif len(same_source_hits) >= 2:
        difference_in_score = same_source_hits[0].get('_score') - same_source_hits[1].get('_score')
        priority0 = same_source_hits[0].get('_source').get('priority')
        priority1 = same_source_hits[1].get('_source').get('priority')
        if difference_in_score == 0 and priority0 != priority1:
            difference_in_score = 99
            if priority1 > priority0:
                hits[0] = same_source_hits[1]
    else:
        difference_in_score = 99

    if not max_score or max_score < min_needed_score or difference_in_score < 0.65:
        return None, 0

    wanted_result: dict = hits[0].get('_source')
    return SeretMovieInfo(wanted_result.get('english_name').strip(), wanted_result.get('name').strip(),
                          wanted_result.get('description').strip(), wanted_result.get('image_url'),
                          wanted_result.get('year')), max_score
