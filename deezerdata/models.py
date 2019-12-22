from django.db import models

from musicdata.models import *

class DeezerAlbum(Release):
    """
    Represents an album in Deezer's database.
    """
    dz_id = models.BigIntegerField()
    link = models.URLField(max_length=2000)
    share = models.URLField(max_length=2000)
    cover_small = models.URLField(max_length=2000, 
            null=True, blank=True)
    cover_medium = models.URLField(max_length=2000, 
            null=True, blank=True)
    cover_big = models.URLField(max_length=2000, 
            null=True, blank=True)
    cover_xl = models.URLField(max_length=2000, 
            null=True, blank=True)
    nb_tracks = models.IntegerField()
    duration = models.IntegerField()
    nb_fans = models.IntegerField()
    rating = models.IntegerField()
    available = models.BooleanField()
    alternative_id = models.BigIntegerField(null=True, blank=True)
    tracklist_url = models.URLField(max_length=2000, 
            null=True, blank=True)
    explicit_lyrics = models.BooleanField()
    explicit_content_lyrics = models.IntegerField()
    explicit_content_cover = models.IntegerField()
    
    
class DeezerTrack(Track):
    dz_id = models.BigIntegerField()
    release = models.ForeignKey('DeezerAlbum', on_delete=models.PROTECT,
        related_name='tracks')
    readable = models.BooleanField()
    title_short = models.CharField(max_length=1000)
    title_version = models.CharField(max_length=1000)
    unseen = models.BooleanField()
    link = models.URLField(max_length=2000)
    rank = models.BigIntegerField()
    release_date = models.DateField()
    explicit_lyrics = models.BooleanField()
    explicit_content_lyrics = models.IntegerField()
    explicit_content_cover = models.IntegerField()
    preview = models.URLField(max_length=2000)
    bpm = models.FloatField()  # Not included in Recording
                                   # as it is part of audio features.
    gain = models.FloatField()
    alternative_id = models.BigIntegerField(null=True, blank=True)
    
    
class DeezerMp3(DeezerTrack):
    title = models.CharField(max_length=1000)
    artist_name = models.CharField(max_length=500)
    album_name = models.CharField(max_length=1000)
    
