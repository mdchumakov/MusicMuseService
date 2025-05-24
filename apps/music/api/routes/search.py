from loguru import logger
from ninja import Router
from ninja.throttling import AnonRateThrottle, AuthRateThrottle

from apps.music.api.docs import Tags
from apps.music.api.dto.search import SearchEntityType, SearchOutSchema
from apps.music.documents import ArtistsDocument, ReleaseDocument, TracksDocument

router_v1 = Router(tags=[Tags.search])


@router_v1.get(
    path="",
    tags=[Tags.search],
    summary="Поиск по артистам, трекам и релизам",
    auth=None,
    throttle=[AnonRateThrottle("100/s"), AuthRateThrottle("100/s")],
)
def search(request, q: str) -> list[SearchOutSchema]:
    logger.info(request)

    documents = [
        {"document": TracksDocument, "type": SearchEntityType.track},
        {"document": ArtistsDocument, "type": SearchEntityType.artist},
        {"document": ReleaseDocument, "type": SearchEntityType.release},
    ]
    result_response = []
    for document in documents:
        doc, doc_type = document["document"], document["type"]

        search_ = doc.search()
        search_query = search_.query(_query(query=q))
        search_response = [
            SearchOutSchema(
                entity_id=hit.meta.id,
                name=hit.name,
                entity=doc_type,
                score=hit.meta.score,
            )
            for hit in search_query.execute()
        ]
        result_response.extend(search_response)

    result_response.sort(key=lambda el: el.score, reverse=True)

    return result_response[:10]


def _query(query: str) -> dict:
    return {
        "multi_match": {
            "query": query,
            "fields": ["name", "name.suggest"],
            "type": "best_fields",
            "fuzziness": "AUTO",
        }
    }
