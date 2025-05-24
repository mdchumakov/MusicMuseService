from django_opensearch_dsl import Document
from django_opensearch_dsl.registries import registry

from apps.music.models import Artists, Releases, Tracks


@registry.register_document
class TracksDocument(Document):
    class Index:
        name = "tracks"  # Name of the Opensearch index
        settings = {  # See Opensearch Indices API reference for available settings
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }
        # Configure how the index should be refreshed after an update.
        # See Opensearch documentation for supported options.
        # This per-Document setting overrides settings.OPENSEARCH_DSL_AUTO_REFRESH.
        auto_refresh = True

    class Django:
        model = Tracks  # The model associated with this Document
        fields = [  # The fields of the model you want to be indexed in Opensearch
            "name",
        ]
        # Paginate the Django queryset used to po
        #
        #
        #
        # pulate the index with the specified size
        # This per-Document setting overrides settings.OPENSEARCH_DSL_QUERYSET_PAGINATION.
        queryset_pagination = 5000


@registry.register_document
class ArtistsDocument(Document):
    class Index:
        name = "artists"
        settings = {  # See Opensearch Indices API reference for available settings
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }
        auto_refresh = True

    class Django:
        model = Artists  # The model associated with this Document
        fields = [  # The fields of the model you want to be indexed in Opensearch
            "name",
        ]
        # Paginate the Django queryset used to populate the index with the specified size
        # This per-Document setting overrides settings.OPENSEARCH_DSL_QUERYSET_PAGINATION.
        queryset_pagination = 5000


@registry.register_document
class ReleaseDocument(Document):
    class Index:
        name = "release"

    class Django:
        model = Releases
        fields = [
            "name",
        ]
        queryset_pagination = 5000
