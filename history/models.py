
import datetime as dt

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone as tz

from deezerdata.models import *


class HistoryEntry(models.Model):
    version = models.IntegerField(default=settings.MH_VERSION)
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    track_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    track = GenericForeignKey('track_type', 'object_id')
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
            dt.datetime.fromtimestamp(entry_json['timestamp']),
            tz.get_current_timezone()
        )
        track_id = entry_json['id']

        if entry_listening_datetime > profile.last_history_request:
            db_entry = HistoryEntry(
                profile=profile,
                dz_timestamp=entry_json['timestamp'],
                listening_datetime=entry_listening_datetime,
            )
            try:
                if track_id > 0:  # Deezer track.
                    track = DeezerTrack.retrieve_from_deezer(track_id)[0]
                    db_entry.entry_type = 'deezer_track'

                else:  # User's mp3
                    track, created = DeezerTrack.objects.get_or_create(
                        dz_id=track_id)
                    if created:
                        track.title = track.title_short = entry_json['title']
                        track.dz_artist_name = entry_json['artist']['name']
                        track.dz_album_title = entry_json['album']['title']
                        track.save()
                    db_entry.entry_type = 'deezer_mp3'

                db_entry.dz_track = track

            except DeezerApiError:
                db_entry.entry_type = 'deezer_error'

            db_entry.save()
        else:
            ignored = True

        return (ignored, entry_listening_datetime)
