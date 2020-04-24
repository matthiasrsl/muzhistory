import datetime as dt

from django.conf import settings
from django.db import models
from django.db.models import Count

from musicdata.models import *
from platform_apis.models import DeezerApiError, Market
from tools.models import log_exceptions


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
    deleted = models.BooleanField(default=False)
    last_update = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.release_group.title} (Deezer)"

    def download_data(self):  # pragma: no cover
        """
        Downloads the album data from the Deezer Api.
        """
        api_request = requests.get(
            settings.DEEZER_API_ALBUM_URL.format(self.dz_id)
        )
        json_data = api_request.json()
        return json_data

    @classmethod
    @log_exceptions
    def get_or_retrieve(cls, dz_id, update=False):
        """
        Retrieves an album from the database with the given id, or,
        if not in the database, makes a request to the Deezer API and creates
        the instance.
        """
        instance, created = cls.objects.get_or_create(dz_id=dz_id)

        try:
            # Fields other than id are set only if a new DeezerAlbum
            # instance was created, or if the instance should be updated.
            if created or update or settings.ALWAYS_UPDATE_DEEZER_DATA:
                json_data = instance.download_data()

                try:
                    error_type = json_data["error"]["type"]
                    message = json_data["error"]["message"]
                    code = json_data["error"]["code"]
                    if created:
                        instance.delete()  # Otherwise, a blank album would
                        # stay in the database.
                        raise DeezerApiError(error_type, message, code)
                    else:
                        instance.deleted = True
                        instance.save()
                        return instance, created
                except KeyError:
                    pass  # No API-related error occured.

                # Creation of the ReleaseGroup. A ReleaseGroup can be
                # uniquely indetified by its title and its set of
                # contributors. If we don't find a ReleaseGroup matching
                # these criteria, we create a new one.
                if (
                    json_data["record_type"]
                    not in ReleaseGroup.AlbumTypeChoices.values
                ):
                    album_type = ReleaseGroup.AlbumTypeChoices.UNDEF
                else:
                    album_type = json_data["record_type"]

                existing_release_groups = (
                    ReleaseGroup.objects.filter(
                        title=json_data["title"], album_type=album_type,
                    )
                    .annotate(contrib_count=Count("contributors"))
                    .filter(contrib_count=len(json_data["contributors"]))
                )
                for json_contrib in json_data["contributors"]:
                    existing_release_groups = existing_release_groups.filter(
                        contributors__deezer_id=json_contrib["id"]
                    )

                if existing_release_groups.count() == 0:
                    release_group = ReleaseGroup.objects.create(
                        title=json_data["title"], album_type=album_type,
                    )
                    rl_created = True
                else:
                    release_group = existing_release_groups[0]
                    rl_created = False

                instance.cover_small = json_data["cover_small"]
                instance.cover_medium = json_data["cover_medium"]
                instance.cover_big = json_data["cover_big"]
                instance.cover_xl = json_data["cover_xl"]
                release_date_list = json_data["release_date"].split("-")
                release_date_list = [int(elt) for elt in release_date_list]
                try:  #  Avoid errors with date 0000-00-00
                    instance.release_date = dt.date(*release_date_list)
                except ValueError:
                    pass  # release_date is set to NULL
                instance.label_name = json_data["label"]
                instance.barcode_type = Release.BarcodeTypeChoices.UPC
                instance.barcode = json_data["upc"]
                instance.link = json_data["link"]
                instance.share = json_data["share"]
                instance.nb_tracks = json_data["nb_tracks"]
                instance.nb_fans = json_data["fans"]
                instance.rating = json_data["rating"]
                instance.duration = json_data["duration"]
                instance.available = json_data["available"]
                instance.tracklist_url = json_data["tracklist"]
                instance.explicit_lyrics = json_data["explicit_lyrics"]
                instance.explicit_content_lyrics = json_data[
                    "explicit_content_lyrics"
                ]
                instance.explicit_content_cover = json_data[
                    "explicit_content_cover"
                ]

                if not instance.available:
                    try:  # Even when the album is not available, the
                        # alternative album is not always present in the
                        # API response.
                        instance.alternative_id = json_data["alternative"][
                            "id"
                        ]
                    except:
                        pass  # The field is set to NULL.

                instance.release_group = release_group
                instance.last_update = tz.now()
                instance.save()

                for json_genre in json_data["genres"]["data"]:
                    genre, genre_created = Genre.objects.get_or_create(
                        dz_id=json_genre["id"]
                    )
                    if genre_created:
                        genre.name = json_genre["name"]
                        genre.save()
                    instance.release_group.genres.add(genre)

                if not rl_created:  #  To avoid duplicate contributions
                    ReleaseGroupContribution.objects.filter(
                        release_group=release_group
                    ).delete()

                for json_contrib in json_data["contributors"]:
                    contributor = Artist.get_or_retrieve_from_deezer(
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
            instance.save()
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
    title = models.CharField(max_length=1000)
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
    deleted = models.BooleanField(default=False)
    last_update = models.DateTimeField(null=True)

    def __str__(self):
        return (
            f"{self.title} (Deezer)" if self.recording else "ERROR"
        )

    def save(self, *args, **kwargs):
        self.track_type = Track.TrackTypeChoices.DEEZER_TRACK
        super().save(*args, **kwargs)

    @classmethod
    def download_deezer_track_by_isrc(cls, isrc):  # pragma: no cover
        """
        Downloads the default Deezer track with this isrc.
        """
        api_request = requests.get(
            settings.DEEZER_API_TRACK_BY_ISRC_URL.format(isrc)
        )
        json_data = api_request.json()
        return json_data

    def download_data(self):  # pragma: no cover
        """
        Downloads the track data from the Deezer Api.
        """
        api_request = requests.get(
            settings.DEEZER_API_TRACK_URL.format(self.dz_id)
        )
        json_data = api_request.json()

        return json_data

    @classmethod
    @log_exceptions
    def get_or_retrieve(cls, dz_id, update=False):
        """
        Retrieves a track from the database with the given id, or, if not
        in the database, makes a request to the Deezer API and creates
        the instance.
        """
        if dz_id < 0:
            raise ValueError("This id corresponds to a Deezer user mp3.")

        instance, created = cls.objects.get_or_create(dz_id=dz_id)

        try:
            # Fields other than id are set only if a new DeezerAlbum
            # instance was created, or if the instance should be updated.
            if created or update or settings.ALWAYS_UPDATE_DEEZER_DATA:
                json_data = instance.download_data()
                try:
                    error_type = json_data["error"]["type"]
                    message = json_data["error"]["message"]
                    code = json_data["error"]["code"]
                    if created:
                        instance.delete()  # Otherwise, a blank track would
                        # stay in the database.
                        raise DeezerApiError(error_type, message, code)
                    else:
                        instance.deleted = True
                        instance.save()
                        return instance, created
                except KeyError:
                    pass  # No API-related error occured.
                
                instance.save()
                recording, recording_created = Recording.objects.get_or_create(
                    isrc=json_data["isrc"]
                )
                recording.save()
                instance.recording = recording

                if (
                    recording_created
                    or update
                    or settings.ALWAYS_UPDATE_DEEZER_DATA
                ):
                    default_deezer_track_json = cls.download_deezer_track_by_isrc(
                        recording.isrc
                    )  #  The default Deezer Track with this ISRC.
                    if default_deezer_track_json["id"] == instance.dz_id:
                        recording.deezer_track = instance
                        recording.title = json_data["title"]
                    else:
                        default_deezer_track, ddt_created = cls.get_or_retrieve(
                            default_deezer_track_json["id"]
                        )
                        recording.deezer_track = default_deezer_track
                        recording.title = default_deezer_track.title

                recording.save()

                try:
                    track_title_version = json_data["title_version"]
                except KeyError:
                    track_title_version = ""
                instance.title_version = track_title_version
                instance.title = json_data["title"]
                instance.title_short = json_data["title_short"]
                instance.duration = json_data["duration"]
                instance.readable = json_data["readable"]
                instance.link = json_data["link"]
                instance.share = json_data["share"]
                instance.rank = json_data["rank"]
                release_date_list = json_data["release_date"].split("-")
                release_date_list = [int(elt) for elt in release_date_list]
                try:  #  Avoid errors with date 0000-00-00
                    instance.release_date = dt.date(*release_date_list)
                except ValueError:
                    pass  # release_date is set to NULL
                instance.disc_number = json_data["disk_number"]
                instance.track_number = json_data["track_position"]
                instance.explicit_lyrics = json_data["explicit_lyrics"]
                instance.explicit_content_lyrics = json_data[
                    "explicit_content_lyrics"
                ]
                instance.explicit_content_cover = json_data[
                    "explicit_content_cover"
                ]
                instance.preview = json_data["preview"]
                instance.bpm = json_data["bpm"]
                instance.gain = json_data["gain"]

                if not instance.readable:
                    try:  # Even when the track is not readable, the
                        # alternative track is not always present in the
                        # API response.
                        instance.alternative_id = json_data["alternative"][
                            "id"
                        ]
                    except:
                        pass  # The field is set to NULL.

                try:
                    instance.release = DeezerAlbum.get_or_retrieve(
                        json_data["album"]["id"]
                    )[0]
                except DeezerApiError:
                    pass  # Orphan track, not a problem.

                if not recording_created:  # To avoid duplicate contributions
                    RecordingContribution.objects.filter(
                        recording=recording
                    ).delete()

                for json_contrib in json_data["contributors"]:
                    contributor = Artist.get_or_retrieve_from_deezer(
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
                for market_code in json_data["available_countries"]:
                    market, market_created = Market.objects.get_or_create(
                        code=market_code
                    )
                    if market_created and settings.LOG_RETRIEVAL:
                        print(f"Market {market.code} created")
                    available_markets.append(market)
                instance.available_markets.add(*available_markets)
                # Bulk-add to reduce database access.

                instance.last_update = tz.now()
                instance.save()

        except:  # If an unexpected error happens, we don't want a
            # corrupted object to pollute the database.
            instance.save()
            instance.delete()
            raise

        if created and settings.LOG_RETRIEVAL:
            print("retrieved track {}.".format(instance))
        return (instance, created)


class DeezerMp3(DeezerTrack):
    artist_name = models.CharField(max_length=500)
    album_name = models.CharField(max_length=1000)
    deezer_account = models.ForeignKey(
        "deezerdata.DeezerAccount", on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.recording.title} (Deezer Mp3)"

    def save(self, *args, **kwargs):
        self.track_type = Track.TrackTypeChoices.DEEZER_MP3
        super(Track, self).save(*args, **kwargs)

    def download_data(self, deezer_account):  # pragma: no cover
        """
        Downloads the track data from the Deezer Api.
        """
        params = {"access_token": deezer_account.access_token}
        api_request = requests.get(
            settings.DEEZER_API_TRACK_URL.format(self.dz_id), params=params
        )
        json_data = api_request.json()

        return json_data

    @classmethod
    def get_or_retrieve(cls, dz_id, deezer_account, update=False):
        """
        Retrieves a mp3 from the database with the given id, or, if not
        in the database, makes a request to the Deezer API and creates
        the instance.
        """
        if dz_id > 0:
            raise ValueError("This id corresponds to a Deezer ragular track.")

        instance, created = cls.objects.get_or_create(
            dz_id=dz_id, deezer_account=deezer_account
        )

        try:
            # Fields other than id are set only if a new DeezerAlbum
            # instance was created, or if the instance should be updated.
            if created or update or settings.ALWAYS_UPDATE_DEEZER_DATA:
                json_data = instance.download_data(deezer_account)

                try:
                    error_type = json_data["error"]["type"]
                    message = json_data["error"]["message"]
                    code = json_data["error"]["code"]
                    if created:
                        instance.delete()  # Otherwise, a blank track would
                        # stay in the database.
                        raise DeezerApiError(error_type, message, code)
                    else:
                        instance.deleted = True
                        instance.save()
                        return instance, created
                except KeyError:  # No API-related error occured.
                    pass

                recording, recording_created = Recording.objects.get_or_create(
                    isrc=json_data["isrc"], title=json_data["title"]
                )
                recording.title = json_data["title"]
                recording.deezer_track = instance
                recording.save()
                instance.recording = recording

                if json_data["isrc"]:
                    raise ValueError("This is not a user mp3.")
                instance.title = instance.title_short = json_data["title"]
                instance.artist_name = json_data["artist"]["name"]
                instance.album_title = json_data["album"]["title"]
                instance.save()

                instance.last_update = tz.now()
                instance.save()

        except:  # If an unexpected error happens, we don't want a
            # corrupted object to pollute the database.
            instance.save()
            instance.delete()
            raise

        if created and settings.LOG_RETRIEVAL:
            print("retrieved track {}.".format(instance))
        return (instance, created)
