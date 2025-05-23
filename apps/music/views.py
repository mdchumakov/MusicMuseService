from http import HTTPStatus
from random import randint

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader

from apps.music.models import Artists, Releases, Tracks
from apps.music.services.popular_extractor import popular_extractor
from apps.music.services.search import make_full_search

_MIN_SEARCH_QUERY_LEN = 3


def download_track(request: HttpRequest, track_id: int):
    track = get_object_or_404(Tracks, id=track_id)

    response_headers = {
        "Content-Disposition": f'attachment; filename="{track.slug}.mp3"',
    }

    return HttpResponse(
        track.track.audio.read(),
        content_type="audio/mp3",
        headers=response_headers,
    )


def music(request: HttpRequest) -> HttpResponse:
    search_query = request.GET.get("q")
    if search_query and len(search_query.strip()) < _MIN_SEARCH_QUERY_LEN:
        no_results = loader.get_template("no_results.html")
        return HttpResponse(no_results.render({"query": search_query}, request))

    template = loader.get_template("music.html")

    if search_query:
        artists, tracks, releases = make_full_search(search_query)
        if all((artists is None, releases is None, tracks is None)):
            no_results = loader.get_template("no_results.html")
            return HttpResponse(no_results.render({"query": search_query}, request))
    else:
        artists, releases, tracks = popular_extractor()

    context = {
        "artists": artists,
        "releases": releases,
        "tracks": tracks,
        "searched": bool(search_query),
    }

    return HttpResponse(template.render(context, request))


def music_artist_page(request: HttpRequest, artist_id: int) -> HttpResponse:
    if request.GET.get("q"):
        return music(request)

    try:
        artist = Artists.objects.get(pk=artist_id)
    except Artists.DoesNotExist:
        not_found = loader.get_template("404.html")
        return HttpResponse(
            status=HTTPStatus.NOT_FOUND,
            content=not_found.render({}, request),
        )
    template = loader.get_template("music_artist.html")

    popular_tracks = Tracks.objects.filter(artists__id=artist_id).order_by("-created")[:10]
    releases = Releases.objects.filter(artists__in=[artist])[:10]
    context = {
        "artist": artist,
        "tracks": popular_tracks,
        "releases": releases,
        "monthly_listeners": randint(1, 100),
    }

    return HttpResponse(template.render(context, request))


def music_track_page(request: HttpRequest, track_id: int) -> HttpResponse:
    if request.GET.get("q"):
        return music(request)

    try:
        track = Tracks.objects.get(pk=track_id)
    except Tracks.DoesNotExist:
        not_found = loader.get_template("404.html")
        return HttpResponse(
            status=HTTPStatus.NOT_FOUND,
            content=not_found.render({}, request),
        )

    template = loader.get_template("track_detail.html")
    release_tracks = Tracks.objects.filter(release__id=track.release.pk)

    context = {
        "track": track,
        "tracks": release_tracks,
        "total_duration": _calculate_total_duration(release_tracks),
    }

    return HttpResponse(template.render(context, request))


def music_release_page(request: HttpRequest, release_id: int) -> HttpResponse:
    if request.GET.get("q"):
        return music(request)

    try:
        release = Releases.objects.get(pk=release_id)
    except Releases.DoesNotExist:
        not_found = loader.get_template("404.html")
        return HttpResponse(
            status=HTTPStatus.NOT_FOUND,
            content=not_found.render({}, request),
        )

    template = loader.get_template("release_detail.html")

    tracks = Tracks.objects.filter(release__id=release_id)

    context = {
        "release": release,
        "tracks": tracks,
        "total_duration": _calculate_total_duration(tracks),
    }

    return HttpResponse(template.render(context, request))


def _calculate_total_duration(tracks: list[Tracks]) -> str:
    hours_minutes_seconds = "{hours} ч. {minutes} мин. {seconds} сек."
    minutes_seconds = "{minutes} мин. {seconds} сек."

    total_duration = sum(track.track.duration.seconds for track in tracks)
    seconds = f"0{total_duration % 60}" if total_duration % 60 < 10 else total_duration % 60

    if total_duration >= 3600:
        return hours_minutes_seconds.format(
            hours=total_duration // 3600,
            minutes=(total_duration % 3600) // 60,
            seconds=seconds,
        )
    return minutes_seconds.format(
        minutes=total_duration // 60,
        seconds=seconds,
    )
