from django.db import models

from musicdata.models import *

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
    
