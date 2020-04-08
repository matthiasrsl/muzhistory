import datetime as dt

from django.conf import settings
from django.db import models
from django.utils import timezone as tz

from deezerdata.models import *


class SpecialHistoryEntryChoices(models.TextChoices):
    """
    Choices for the different types of HistoryEntry in case of a
    non-track related HistoryEntry (such as retrieval errors, etc.)
    """

    LISTENING = "listening", "Track listening"  # Regular
    DEEZER_ERROR = "err_deezer", "Deezer error"
    DEEZER_ELLIPSIS = "ellipsis", "History Ellipsis (Deezer)"


class HistoryEntry(models.Model):
    """
    An entry in a profile's listening history, generally corresponding
    to the listening of a track.
    """

    version = models.IntegerField(default=settings.MH_VERSION)
    profile = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    entry_type = models.CharField(
        max_length=100,
        choices=SpecialHistoryEntryChoices.choices,
        default=SpecialHistoryEntryChoices.LISTENING,
    )
    track = models.ForeignKey("musicdata.Track", on_delete=models.PROTECT)
    timestamp = models.PositiveIntegerField(null=True, blank=True)
    # Consistent with timestamp if it is not null.
    listening_datetime = models.DateTimeField()

    @classmethod
    def new_deezer_track_entry(cls, entry_json, profile):
        """
        Creates, if not existing, a new HistoryEntry corresponding to
        the provided json data from the Deezer API.
        """
        ignored = False  #  Default value
        entry_text = str(entry_json)
        entry_listening_datetime = tz.make_aware(
            dt.datetime.fromtimestamp(entry_json["timestamp"]),
            tz.get_current_timezone(),
        )
        track_id = entry_json["id"]

        if entry_listening_datetime > profile.last_history_request:
            db_entry = HistoryEntry(
                profile=profile,
                timestamp=entry_json["timestamp"],
                listening_datetime=entry_listening_datetime,
            )
            try:
                if track_id > 0:  # Deezer track.
                    track = DeezerTrack.retrieve(track_id)[0]

                else:  # User's mp3
                    mp3, created = DeezerMp3.objects.get_or_create(
                        dz_id=track_id
                    )
                    if created:
                        mp3.title = track.title_short = entry_json["title"]
                        mp3.artist_name = entry_json["artist"]["name"]
                        mp3.album_title = entry_json["album"]["title"]
                        mp3.save()

                db_entry.track = track

            except DeezerApiError:
                db_entry.entry_type = SpecialHistoryEntryChoices.LISTENING

            db_entry.save()
        else:
            ignored = True

        return ignored, entry_listening_datetime
