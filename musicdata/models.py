import json

from django.conf import settings
from django.db import models
from django.utils import timezone as tz

import requests
from platform_apis.models import DeezerApiError
from tools.models import log_exceptions

# from deezerdata import DeezerTrack



class ImpossibleMerge(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "Unable to merge objects."


class Artist(models.Model):
    """
    Represents an artist. 
    Not platform-dependent.
    """

    version = models.IntegerField(default=settings.MH_VERSION)
    name = models.CharField(max_length=500)
    deezer_id = models.BigIntegerField(null=True, blank=True)
    spotify_id = models.CharField(max_length=50)
    image_url_deezer_xl = models.URLField(max_length=2000)
    image_url_deezer_big = models.URLField(max_length=2000)
    image_url_deezer_medium = models.URLField(max_length=2000)
    image_url_deezer_small = models.URLField(max_length=2000)
    image_url_spotify_largest = models.URLField(max_length=2000)
    # The sizes vary on Spotify.
    image_url_spotify_medium = models.URLField(max_length=2000)
    nb_fans_deezer = models.BigIntegerField(null=True, blank=True)
    deleted_deezer = models.BooleanField(default=False)
    last_update_deezer = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.name} (Artist)"

    def merge(self, artist):
        if self.name != artist.name:
            raise ImpossibleMerge
        else:
            pass

    def download_data_from_deezer(self):  # pragma: no cover
        """
        Downloads the artist data from the Deezer Api.
        """
        r_artist = requests.get(
            settings.DEEZER_API_ARTIST_URL.format(self.deezer_id)
        )
        json_data = r_artist.json()

        return json_data

    @classmethod
    @log_exceptions
    def get_or_retrieve_from_deezer(cls, dz_id, update=False):
        """
        Retrieves an artist from the database with the given id, or,
        if not in the database, makes a request to the Deezer API and creates
        the instance.
        """
        instance, created = cls.objects.get_or_create(deezer_id=dz_id)

        try:
            # Fields other than id are set only if a new Artist instance
            # was created, or if the instance should be updated.
            if created or update or settings.ALWAYS_UPDATE_DEEZER_DATA:
                json_data = instance.download_data_from_deezer()

                try:
                    error_type = json_data["error"]["type"]
                    message = json_data["error"]["message"]
                    code = json_data["error"]["code"]
                    if created:
                        instance.delete()  # Otherwise, a blank artist would
                                           # stay in the database.
                        raise DeezerApiError(error_type, message, code)
                    else:
                        instance.deleted_deezer = True
                        instance.save()
                        return instance, created
                except KeyError:
                    pass  # No API-related error occured.

                    instance.name = json_data["name"]
                    instance.image_url_deezer_small = json_data["picture_small"]
                    instance.image_url_deezer_medium = json_data["picture_medium"]
                    instance.image_url_deezer_big = json_data["picture_big"]
                    instance.image_url_deezer_xl = json_data["picture_xl"]
                    instance.nb_fans_deezer = json_data["nb_fan"]
                    instance.last_update_deezer = tz.now()
                    instance.save()


            if created and settings.LOG_RETRIEVAL:
                print("retrieved artist {}.".format(instance))
            return (instance, created)
        except:  # If an unexpected error happens, we don't want a
            # corrupted object to pollute the database.
            instance.save()  # To be able to delete it.
            instance.delete()
            raise


class ReleaseGroup(models.Model):
    """
    Represents an "album", independently of the medium on which it is released.
    Therefore, it is not platform-dependent.
    Corresponds to a MusicBrainz release group.
    """

    version = models.IntegerField(default=settings.MH_VERSION)

    class AlbumTypeChoices(models.TextChoices):
        SINGLE = "single", "single"
        ALBUM = "album", "album"
        EP = "EP", "EP"
        COMPILATION = "compilation", "compilation"
        UNDEF = "undef", "undefined"

    title = models.CharField(max_length=1000)
    album_type = models.CharField(
        max_length=100,
        choices=AlbumTypeChoices.choices,
        default=AlbumTypeChoices.UNDEF,
    )
    genres = models.ManyToManyField('Genre')
    contributors = models.ManyToManyField(
        "Artist", through="ReleaseGroupContribution"
    )

    def __str__(self):
        return f"{self.title} (Release group)"

    def merge(self, release_group):
        pass


class Release(models.Model):
    """
    Represents a release of an "album" (i.e. ReleaseGroup).
    It is therefore platform-dependent, that's why this is an abstract model.
    This model does not exactly corresponds to a MusicBrainz Release, but
    rather a Release plus a Medium.
    """

    version = models.IntegerField(default=settings.MH_VERSION)

    class BarcodeTypeChoices(models.TextChoices):
        UPC = ("upc", "UPC")
        NONE = ("none", "No barcode")
        UNDEF = ("undef", "Undefined")

    release_group = models.ForeignKey(
        "musicdata.ReleaseGroup",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    barcode = models.CharField(max_length=30)
    barcode_type = models.CharField(
        max_length=30, choices=BarcodeTypeChoices.choices, default="none"
    )
    release_date = models.DateField(null=True, blank=True)
    label_name = models.CharField(max_length=1000)

    class Meta:
        abstract = True


class Recording(models.Model):
    """
    Represents a piece of music, independently of the album (i.e. Release) on
    which it is released. It is therefore not platform-dependent.
    A Recording can be uniquely identified by its ISRC.
    It corresponds to a MusicBrainz's Recording.
    """

    version = models.IntegerField(default=settings.MH_VERSION)
    isrc = models.CharField(max_length=12)
    title = models.CharField(max_length=1000)

    # Tracks from which the platform-specific data come from.
    # If the Track is deleted, the platform-specific information will
    # no longer be available. As this data is not critically
    # important, we allow this behaviour (which is better than having
    # tracks - and therefore potentially history entries - having no
    # recording).
    deezer_track = models.ForeignKey(
        "deezerdata.DeezerTrack",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    # spotify_track = models.ForeignKey(...)

    contributors = models.ManyToManyField(
        "Artist", through="RecordingContribution"
    )

    def __str__(self):
        return f"{self.title} ({self.isrc})"


class Track(models.Model):
    """
    A Track represents the way a Recording is included on a Release.
    Like a Release, it is platform-dependent, and it is therefore an abstract
    model.
    It corresponds to a MusicBrainz's Track.
    """

    class TrackTypeChoices(models.TextChoices):
        DEEZER_TRACK = "deezer_track", "Deezer track"
        DEEZER_MP3 = "deezer_mp3", "Deezer user's mp3"

    version = models.IntegerField(default=settings.MH_VERSION)
    track_type = models.CharField(
        max_length=20, choices=TrackTypeChoices.choices
    )
    recording = models.ForeignKey(
        "musicdata.Recording", on_delete=models.PROTECT, null=True, blank=True
    )
    disc_number = models.IntegerField(null=True, blank=True)
    # Position on the disc.
    track_number = models.IntegerField(null=True, blank=True)
    available_markets = models.ManyToManyField("platform_apis.Market")

    def __str__(self):
        if self.track_type == self.TrackTypeChoices.DEEZER_TRACK:
            return str(self.deezertrack)
        elif self.track_type == self.TrackTypeChoices.DEEZER_MP3:
            return str(self.deezertrack.deezermp3)
        else:
            return super().__str__()


class Genre(models.Model):
    version = models.IntegerField(default=settings.MH_VERSION)
    name = models.CharField(max_length=100)
    dz_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Contribution(models.Model):
    """
    Intermediary model for M2M between a Artist and either a Recording or a
    ReleaseGroup.
    """

    version = models.IntegerField(default=settings.MH_VERSION)
    role_choices = [
        ("main", "main"),
        ("feat", "featured"),
        ("undef", "undefined"),
    ]
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20, choices=role_choices, default="undef"
    )

    class Meta:
        abstract = True


class ReleaseGroupContribution(Contribution):
    """
    Intermediary model for M2M between a Artist and a ReleaseGroup.
    """
    release_group = models.ForeignKey("ReleaseGroup", on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.artist.name} as {self.role} on RG "
            f"{self.release_group.title}"
        )


class RecordingContribution(Contribution):
    """
    Intermediary model for M2M between a Artist and a Recording.
    """

    recording = models.ForeignKey("Recording", on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.artist.name} as {self.role} on Rec. "
            "{self.recording.title}"
        )
