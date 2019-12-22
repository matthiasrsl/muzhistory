from django.db import models
import datetime as dt

from musicdata.models import *
from platform_apis.models import DeezerApiError

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

    @classmethod
    def retrieve(cls, dz_id):
        """
        Retrieves an album from the database with the given id, or,
        if not in the database, makes a request to the Deezer API and creates
        the instance.
        """
        instance, created = cls.objects.get_or_create(
                dz_id=dz_id) 
                
        if created or settings.ALWAYS_UPDATE_DEEZER_DATA:
            # Fields other than id are set only if a new DeezerAlbum
            # instance was created, or if settings.ALWAYS_UPDATE_DEEZER_DATA
            # is set to True.
            r_album = requests.get(
                settings.DEEZER_API_ALBUM_URL.format(
                instance.dz_id)
            )
            json_album = json.loads(r_album.text)
            
            try:
                error_type = json_album['error']['type']
                message = json_album['error']['message']
                code = json_album['error']['code']
                instance.delete() # Otherwise, a blank album will stay in
                                  # the database.
                raise DeezerApiError(error_type, message, code)
            except KeyError:
                # No API-related error occured.
                pass
                
            try:
                artist = Artist.retrieve_from_deezer(
                        json_album['artist']['id']
                )[0]
            except DeezerApiError:
                pass  # ??
            
            # Creation of the ReleaseGroup. A new ReleaseGroup is created
            # each time, we assume that the duplicates will be merged by a
            # cron task.
            if (json_album['record_type'] not in \
                    ReleaseGroup.AlbumTypeChoices.values):
                album_type = ReleaseGroup.AlbumTypeChoices.UNDEF
            else:
                album_type=json_album['record_type']
                
            release_group = ReleaseGroup.objects.create(
                title=json_album['title'],
                album_type=album_type
            )
            
            #for contributor in release_group.contrib
                    
            
            instance.cover_small = json_album['cover_small']
            instance.cover_medium = json_album['cover_medium']
            instance.cover_big = json_album['cover_big']
            instance.cover_xl = json_album['cover_xl']
            release_date_list = json_album['release_date'].split('-')
            release_date_list = [int(elt) for elt in release_date_list]
            instance.release_date = dt.date(*release_date_list)
            instance.label_name = json_album['label']
            instance.barcode_type = Release.BarcodeTypeChoices.UPC
            instance.barcode = json_album['upc']
            instance.release_group = release_group
            instance.save()
        if (created and settings.LOG_RETRIEVAL):
            print("retrieved album {}.".format(instance))
        return (instance, created)
    
class DeezerTrack(Track):
    dz_id = models.BigIntegerField()
    release = models.ForeignKey('DeezerAlbum', on_delete=models.PROTECT,
        related_name='tracks')
    readable = models.BooleanField(null=True, blank=True)
    title_short = models.CharField(max_length=1000)
    title_version = models.CharField(max_length=1000)
    unseen = models.BooleanField(null=True, blank=True)
    link = models.URLField(max_length=2000)
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
    
    
class DeezerMp3(DeezerTrack):
    title = models.CharField(max_length=1000)
    artist_name = models.CharField(max_length=500)
    album_name = models.CharField(max_length=1000)
    
