from django import template
from django.conf import settings

from musicdata.models import Track, Recording, Artist

register = template.Library()


@register.inclusion_tag("history/track_snippet.html")
def track(track, additional_info="", as_recording=False):
    """
    Includes the metadata about a track.
    """
    if not isinstance(track, Track):
        raise template.TemplateSyntaxError(
            "The first argument must be a Track instance "
            "(from musicdata.models)."
        )
    return {
        "track": track,
        "additional_info": str(additional_info),
        "as_recording": bool(as_recording),
        "DEFAULT_ALBUM_COVER_URL": settings.DEFAULT_ALBUM_COVER_URL,
    }


@register.inclusion_tag("history/track_snippet.html")
def stats_recording(recording):
    """
    """
    if not isinstance(recording, Recording):
        raise template.TemplateSyntaxError(
            "The first argument must be a Recording instance "
            "(from musicdata.models)."
        )

    additional_info = f"{recording.entry_count} écoute"
    if recording.entry_count > 1:
        additional_info += "s"
    return {
        "track": recording.deezer_track,
        "additional_info": additional_info,
        "as_recording": True,
        "DEFAULT_ALBUM_COVER_URL": settings.DEFAULT_ALBUM_COVER_URL,
    }
