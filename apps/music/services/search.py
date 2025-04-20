from collections import defaultdict
from apps.music.models import Artists, Tracks, Releases
from apps.music.api.dto.search import SearchEntityType
from apps.music.documents import TracksDocument, ArtistsDocument, ReleaseDocument


def make_full_search(query: str) -> tuple[Artists, Tracks, Releases]:
    documents = [
        {"document": TracksDocument, "type": SearchEntityType.track},
        {"document": ArtistsDocument, "type": SearchEntityType.artist},
        {"document": ReleaseDocument, "type": SearchEntityType.release},
    ]
    opensearch_response = defaultdict(list)
    for document in documents:
        doc, doc_type = document["document"], document["type"]

        search_ = doc.search()
        search_query = search_.query({
                "multi_match": {
                    "query": query,
                    "fields": ["name", "name.suggest"],
                    "type": "best_fields",
                    "fuzziness": "AUTO",
                }
            }
        )
        search_response = [
            dict(
                entity_id=hit.meta.id,
                name=hit.name,
                entity=doc_type,
                score=hit.meta.score,
            )
            for hit in search_query.execute()
        ]
        search_response.sort(key=lambda hit: hit["score"], reverse=True)
        search_response = search_response[:10]
        opensearch_response[doc_type].extend(search_response)

    response = {}
    if opensearch_response[SearchEntityType.artist]:
        ids = [doc["entity_id"] for doc in opensearch_response[SearchEntityType.artist]]
        response["artists"] = Artists.objects.filter(id__in=ids)

    if opensearch_response[SearchEntityType.track]:
        ids = [doc["entity_id"] for doc in opensearch_response[SearchEntityType.track]]
        response["tracks"] = Tracks.objects.filter(id__in=ids)

    if opensearch_response[SearchEntityType.release]:
        ids = [doc["entity_id"] for doc in opensearch_response[SearchEntityType.release]]
        response["releases"] = Releases.objects.filter(id__in=ids)

    return response.get("artists"), response.get("tracks"), response.get("releases")
