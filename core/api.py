from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI
from ninja.throttling import AnonRateThrottle, AuthRateThrottle
from ninja_apikey.security import APIKeyAuth

from apps.music.api.routes.artists import router_v1 as artists_router_v1
from apps.music.api.routes.content import router_v1 as content_router_v1
from apps.music.api.routes.genres import router_v1 as genres_router_v1
from apps.music.api.routes.labels import router_v1 as labels_router_v1
from apps.music.api.routes.releases import router_v1 as releases_router_v1
from apps.music.api.routes.tracks import router_v1 as tracks_router_v1
from apps.music.api.routes.search import router_v1 as search_router_v1
from core.settings import DEBUG, PROJECT_VERSION

api = NinjaAPI(
    docs_decorator=staff_member_required if not DEBUG else None,
    title="MusicMuse REST API",
    version=PROJECT_VERSION,
    description="REST API for MusicMuse project",
    throttle=[
        AnonRateThrottle("2/s") if not DEBUG else AnonRateThrottle("1000/s"),
        AuthRateThrottle("100/s"),
    ],
    auth=APIKeyAuth() if not DEBUG else None,
)

api.add_router(prefix="v1/music/search", router=search_router_v1)
api.add_router(prefix="v1/music/genres", router=genres_router_v1)
api.add_router(prefix="v1/music/artists", router=artists_router_v1)
api.add_router(prefix="v1/music/labels", router=labels_router_v1)
api.add_router(prefix="v1/music/releases", router=releases_router_v1)
api.add_router(prefix="v1/music/tracks", router=tracks_router_v1)
api.add_router(prefix="v1/music/content", router=content_router_v1)
