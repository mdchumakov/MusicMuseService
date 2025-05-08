"""
URL configuration for music_muse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from pictures.conf import get_settings

from apps.music.views import music as music_views
from apps.music.views import music_artist_page as music_artist_page_views
from apps.music.views import music_track_page as music_track_page_views
from apps.music.views import music_release_page as music_release_page_views
from apps.music.views import download_track as download_track_views
from core.api import api
from core.settings import HEALTH_SECRET_TOKEN
from core.views import index
from apps.music.sitemaps import StaticViewSitemap, ArtistSitemap, TrackSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'artists': ArtistSitemap,
    'tracks': TrackSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path("", index, name="index"),
    path("music/", music_views, name="music"),
    path("music/artist/<int:artist_id>/", music_artist_page_views, name="music_artist_page"),
    path("music/track/<int:track_id>/", music_track_page_views, name="music_track"),
    path('music/release/<int:release_id>/', music_release_page_views, name='release_detail'),
    path("music/download/<int:track_id>/", download_track_views, name="download_track"),
    path("api/", api.urls),
    path(rf"ht/{HEALTH_SECRET_TOKEN}/", include("health_check.urls")),
]

if get_settings().USE_PLACEHOLDERS:
    urlpatterns.append(
        path("_pictures/", include("pictures.urls")),
    )
