import datetime as dt

from django.conf import settings
from django.db import models

#from history.models import HistoryEntry
from musicdata.models import *
from platform_apis.models import DeezerApiError, Market


class DeezerAlbum(Release):
    """
    Represents an album in Deezer's database.
    """

    dz_id = models.BigIntegerField()
    link = models.URLField(max_length=2000)
    share = models.URLField(max_length=2000)
    cover_small = models.URLField(max_length=2000)
    cover_medium = models.URLField(max_length=2000)
    cover_big = models.URLField(max_length=2000)
    cover_xl = models.URLField(max_length=2000)
    nb_tracks = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    nb_fans = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    available = models.BooleanField(null=True, blank=True)
    alternative_id = models.BigIntegerField(null=True, blank=True)
    tracklist_url = models.URLField(max_length=2000)
    explicit_lyrics = models.BooleanField(null=True, blank=True)
    explicit_content_lyrics = models.IntegerField(null=True, blank=True)
    explicit_content_cover = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.release_group.title} (Deezer)"

    @classmethod
    def retrieve(cls, dz_id, update=False):
        """
        Retrieves an album from the database with the given id, or,
        if not in the database, makes a request to the Deezer API and creates
        the instance.
        """
        instance, created = cls.objects.get_or_create(dz_id=dz_id)

        if created or update or settings.ALWAYS_UPDATE_DEEZER_DATA:
            # Fields other than id are set only if a new DeezerAlbum
            # instance was created, or if the instance should be updated.
            r_album = requests.get(
                settings.DEEZER_API_ALBUM_URL.format(instance.dz_id)
            )
            json_object = r_album.json()

            try:
                error_type = json_object["error"]["type"]
                message = json_object["error"]["message"]
                code = json_object["error"]["code"]
                instance.delete()  # Otherwise, a blank album will stay in
                # the database.
                raise DeezerApiError(error_type, message, code)
            except KeyError:
                pass  # No API-related error occured.

            try:
                # Creation of the ReleaseGroup. A new ReleaseGroup is created
                # each time, we assume that the duplicates will be merged by a
                # cron task.
                if (
                    json_object["record_type"]
                    not in ReleaseGroup.AlbumTypeChoices.values
                ):
                    album_type = ReleaseGroup.AlbumTypeChoices.UNDEF
                else:
                    album_type = json_object["record_type"]

                release_group = ReleaseGroup.objects.create(
                    title=json_object["title"], album_type=album_type,
                )

                instance.cover_small = json_object["cover_small"]
                instance.cover_medium = json_object["cover_medium"]
                instance.cover_big = json_object["cover_big"]
                instance.cover_xl = json_object["cover_xl"]
                release_date_list = json_object["release_date"].split("-")
                release_date_list = [int(elt) for elt in release_date_list]
                instance.release_date = dt.date(*release_date_list)
                instance.label_name = json_object["label"]
                instance.barcode_type = Release.BarcodeTypeChoices.UPC
                instance.barcode = json_object["upc"]
                instance.link = json_object["link"]
                instance.share = json_object["share"]
                instance.nb_tracks = json_object["nb_tracks"]
                instance.nb_fans = json_object["fans"]
                instance.rating = json_object["rating"]
                instance.duration = json_object["duration"]
                instance.available = json_object["available"]
                if not instance.available:
                    instance.alternative_id = json_object["alternative"]["id"]
                instance.tracklist_url = json_object["tracklist"]
                instance.explicit_lyrics = json_object["explicit_lyrics"]
                instance.explicit_content_lyrics = json_object[
                    "explicit_content_lyrics"
                ]
                instance.explicit_content_cover = json_object[
                    "explicit_content_cover"
                ]

                instance.release_group = release_group
                instance.save()

                for json_contrib in json_object["contributors"]:
                    contributor = Artist.retrieve_from_deezer(
                        json_contrib["id"]
                    )[0]
                    if json_contrib["role"] == "Main":
                        role = "main"
                    elif json_contrib["role"] == "Featured":
                        role = "feat"
                    else:
                        role = "undef"
                    contrib = ReleaseGroupContribution.objects.create(
                        artist=contributor,
                        release_group=release_group,
                        role=role,
                    )
                    contrib.save()

            except:  # If an unexpected error happens, we don't want a
                # corrupted object to pollute the database.
                instance.delete()
                raise

        if created and settings.LOG_RETRIEVAL:
            print("retrieved album {}.".format(instance))
        return (instance, created)


class DeezerTrack(Track):
    # version = models.IntegerField(default=settings.MH_VERSION)
    dz_id = models.BigIntegerField()
    duration = models.IntegerField(null=True, blank=True)
    release = models.ForeignKey(
        "DeezerAlbum",
        on_delete=models.PROTECT,
        related_name="tracks",
        null=True,
        blank=True,
    )
    readable = models.BooleanField(null=True, blank=True)
    title_short = models.CharField(max_length=1000)
    title_version = models.CharField(max_length=1000)
    link = models.URLField(max_length=2000)
    share = models.URLField(max_length=2000)
    rank = models.BigIntegerField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    explicit_lyrics = models.BooleanField(null=True, blank=True)
    explicit_content_lyrics = models.IntegerField(null=True, blank=True)
    explicit_content_cover = models.IntegerField(null=True, blank=True)
    preview = models.URLField(max_length=2000)
    bpm = models.FloatField(null=True, blank=True)  # Not included in Recording
    # as it is part of audio features.
    gain = models.FloatField(null=True, blank=True)
    alternative_id = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.recording.title} (Deezer)"

    @classmethod
    def retrieve(cls, dz_id, update=False):
        """
        Retrieves a track from the database with the given id, or, if not
        in the database, makes a request to the Deezer API and creates
        the instance.
        """
        instance, created = cls.objects.get_or_create(dz_id=dz_id)
        if created or update or settings.ALWAYS_UPDATE_DEEZER_DATA:
            # Fields other than id are set only if a new DeezerAlbum
            # instance was created, or if the instance should be updated.
            r_track = requests.get(
                settings.DEEZER_API_TRACK_URL.format(instance.dz_id)
            )
            json_object = r_track.json()

            try:
                error_type = json_object["error"]["type"]
                message = json_object["error"]["message"]
                code = json_object["error"]["code"]
                instance.delete()  # Otherwise, a blank track would stay in
                # the database.
                raise DeezerApiError(error_type, message, code)
            except KeyError:
                pass  # No API-related error occured.

            try:
                recording, recording_created = Recording.objects.get_or_create(
                    isrc=json_object["isrc"]
                )
                instance.recording = recording

                if (
                    recording_created
                    or update
                    or settings.ALWAYS_UPDATE_DEEZER_DATA
                ):

                    recording.title = json_object["title"]
                    recording.deezer_track = instance
                recording.save()

                try:
                    track_title_version = json_object["title_version"]
                except KeyError:
                    track_title_version = ""
                instance.title_version = track_title_version
                instance.title_short = json_object["title_short"]
                instance.duration = json_object["duration"]
                instance.readable = json_object["readable"]
                instance.link = json_object["link"]
                instance.share = json_object["share"]
                instance.rank = json_object["rank"]
                release_date_list = json_object["release_date"].split("-")
                release_date_list = [int(elt) for elt in release_date_list]
                instance.release_date = dt.date(*release_date_list)
                instance.disc_number = json_object["disk_number"]
                instance.track_number = json_object["track_position"]
                instance.explicit_lyrics = json_object["explicit_lyrics"]
                instance.explicit_content_lyrics = json_object[
                    "explicit_content_lyrics"
                ]
                instance.explicit_content_cover = json_object[
                    "explicit_content_cover"
                ]
                instance.preview = json_object["preview"]
                instance.bpm = json_object["bpm"]
                instance.gain = json_object["gain"]

                if not instance.readable:
                    try:  # Even when the track is not readable, the
                        # alternative track is not always present in the
                        # API response.
                        instance.alternative_id = json_object["alternative"][
                            "id"
                        ]
                    except:
                        pass  # The field is set to NULL.

                try:
                    instance.release = DeezerAlbum.retrieve(
                        json_object["album"]["id"]
                    )[0]
                except DeezerApiError:
                    pass  # Orphan track, not a problem.

                for json_contrib in json_object["contributors"]:
                    contributor = Artist.retrieve_from_deezer(
                        json_contrib["id"]
                    )[0]
                    if json_contrib["role"] == "Main":
                        role = "main"
                    elif json_contrib["role"] == "Featured":
                        role = "feat"
                    else:
                        role = "undef"
                    contrib = RecordingContribution.objects.create(
                        artist=contributor, recording=recording, role=role
                    )
                    contrib.save()

                available_markets = []
                for market_code in json_object["available_countries"]:
                    market, market_created = Market.objects.get_or_create(
                        code=market_code
                    )
                    if market_created and settings.LOG_RETRIEVAL:
                        print(
                            f"Market {market.code} created"
                        )
                    available_markets.append(market)
                instance.available_markets.add(*available_markets)
                # Bulk-add to reduce database access.

                instance.save()

            except:  # If an unexpected error happens, we don't want a
                # corrupted object to pollute the database.
                instance.delete()
                raise

        if created and settings.LOG_RETRIEVAL:
            print("retrieved album {}.".format(instance))
        return (instance, created)


class DeezerMp3(DeezerTrack):
    title = models.CharField(max_length=1000)
    artist_name = models.CharField(max_length=500)
    album_name = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.title} (Deezer Mp3)"