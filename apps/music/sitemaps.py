from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Artists, Releases, Tracks


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "daily"
    protocol = "https"

    def items(self):
        return ["music", "index"]

    def location(self, item):
        return reverse(item)


class ArtistSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Artists.objects.all().order_by("id")

    def location(self, obj):
        return reverse("music_artist_page", args=[obj.id])

    def lastmod(self, obj):
        return obj.updated


class TrackSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Tracks.objects.all().order_by("id")

    def location(self, obj):
        return reverse("music_track", args=[obj.id])

    def lastmod(self, obj):
        return obj.updated


class ReleaseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Releases.objects.all().order_by("id")

    def location(self, obj):
        return reverse("release_detail", args=[obj.id])

    def lastmod(self, obj):
        return obj.updated
