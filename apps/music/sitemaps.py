from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Artists, Tracks


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['music', 'index']

    def location(self, item):
        return reverse(item)


class ArtistSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Artists.objects.all()

    def location(self, obj):
        return reverse('music_artist_page', args=[obj.id])

    def lastmod(self, obj):
        return obj.updated


class TrackSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Tracks.objects.all()

    def location(self, obj):
        return reverse('music_track', args=[obj.id])

    def lastmod(self, obj):
        return obj.updated


