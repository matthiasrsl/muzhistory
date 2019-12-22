import requests
from django.db import models
from django.conf import settings
from django.utils import timezone as tz

from platform_apis.models import DeezerApiError

class ImpossibleMerge(Exception):
    def __init__(self):
        pass
        
    def __str__(self):
        return "Unable to merge objects."
        

class Market(models.Model):
    version = models.IntegerField(default=settings.MH_VERSION)
    code = models.CharField(max_length=2)  # ISO 3166-1 alpha-2.
    english_name = models.CharField(max_length=100);


class Artist(models.Model):
    """
    Represents an artist. 
    Not platform-dependent.
    """
    version = models.IntegerField(default=settings.MH_VERSION)
    name = models.CharField(max_length=500)
    deezer_id = models.BigIntegerField(null=True, blank=True)
    spotify_id = models.BigIntegerField(null=True, blank=True)
    image_url_deezer_xl = models.URLField(max_length=2000)
    image_url_deezer_large = models.URLField(max_length=2000)
    image_url_deezer_medium = models.URLField(max_length=2000)
    image_url_deezer_small = models.URLField(max_length=2000)
    image_url_spotify_largest = models.URLField(max_length=2000)
        # The sizes vary on Spotify.
    image_url_spotify_medium = models.URLField(max_length=2000)
    nb_fans_deezer = models.BigIntegerField(null=True, blank=True)
            
    
    def __str__(self):
        return f"{self.name} (Artist)"
        
    def merge(self, artist):
        if self.name != artist.name:
            raise ImpossibleMerge
        else:
            pass  #for rg in self.releasegroup_set.all()
            
    @classmethod
    def retrieve_from_deezer(cls, dz_id):
        """
        Retrieves an artist from the Deezer database with the given id, or,
        if not in the database, makes a request to the Deezer API and creates
        the instance.
        """
        instance, created = cls.objects.get_or_create(
                deezer_id=dz_id)
        if created or settings.ALWAYS_UPDATE_DEEZER_DATA:
                # Fields other than id are set only if a new Artist instance
                # was created, or if settings.ALWAYS_UPDATE_DEEZER_DATA
                # is set to True.
            r_artist = requests.get(
                settings.DEEZER_API_ARTIST_URL.format(
                instance.deezer_id)
            )
            json_artist = json.loads(r_artist.text)
            
            try:
                error_type = json_artist['error']['type']
                message = json_artist['error']['message']
                code = json_artist['error']['code']
                instance.delete() # Otherwise, a blank artist will stay in
                                  # the database.
                raise DeezerApiError(error_type, message, code)
            except KeyError:
                # No API-related error occured.
                pass
                
            instance.name = json_artist['name']
            instance.image_url_deezer_small = json_artist['picture_small']
            instance.image_url_deezer_medium = json_artist['picture_medium']
            instance.image_url_deezer_big = json_artist['picture_big']
            instance.image_url_deezer_xl = json_artist['picture_xl']
            instance.nb_fans_deezer = json_artist['nb_fan']
        instance.save()
        if (created and settings.LOG_RETRIEVAL):
            print("retrieved artist {}.".format(instance))
        return (instance, created)
        
        

class ReleaseGroup(models.Model):
    """
    Represents an "album", independently of the medium on which it is released.
    Therefore, it is not platform-dependent.
    Corresponds to a MusicBrainz release group.
    """
    version = models.IntegerField(default=settings.MH_VERSION)
    album_type_choices = [
            ('single', "single"),
            ('album', "album"),
            ('EP', "EP"),
            ('compilation', "compilation"),
            ('undef', "undefined"),
    ]

    title = models.CharField(max_length=1000)
    album_type = models.CharField(max_length=100, choices=album_type_choices)  
            # Better as ChoiceField ?
    contributors = models.ManyToManyField('Artist',
            through='ReleaseGroupContribution')
    
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
    barcode_type_choices = [
            ('upc', "UPC"),
            ('none', "No barcode"),
            ('undef', "Undefined"),
    ]
    release_group = models.ForeignKey('musicdata.ReleaseGroup',
            on_delete=models.PROTECT)
    barcode = models.CharField(max_length=30)
    barcode_type = models.CharField(max_length=30, 
            choices=barcode_type_choices, default='none')
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
    audio_features = models.TextField()
    audio_analysis = models.TextField()
    # spotify_track  # Spotify track from which audio_analysis and 
                     # audio_features come.
    duration = models.FloatField(default=-1.0)
    contributors = models.ManyToManyField('Artist',
            through='RecordingContribution')
            
            
class Track(models.Model):
    """
    A Track represents the way a Recording is included on a Release.
    Like a Release, it is platform-dependent, and it is therefore an abstract
    model.
    It corresponds to a MusicBrainz's Track.
    """
    version = models.IntegerField(default=settings.MH_VERSION)
    recording = models.ForeignKey('musicdata.Recording', on_delete=models.PROTECT)
    disc_number = models.IntegerField(null=True, blank=True)
    track_number = models.IntegerField(null=True, blank=True)  # Position on the disc.
    available_markets = models.ManyToManyField('musicdata.Market')
    
    class Meta:
        abstract = True


class Genre(models.Model):
    version = models.IntegerField(default=settings.MH_VERSION)
    name = models.CharField(max_length=100)
    dz_id = models.IntegerField(null=True, blank=True)

    
class Contribution(models.Model):
    """
    Intermediary model for M2M between a Artist and either a Recording or a
    ReleaseGroup.
    """
    version = models.IntegerField(default=settings.MH_VERSION)
    role_choices = [
            ('main', "main"),
            ('feat', "featured"),
            ('undef', "undefined")
    ]
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=role_choices,
            default='undef')
    
    class Meta:
        abstract = True

        
class ReleaseGroupContribution(Contribution):
    """
    Intermediary model for M2M between a Artist and a ReleaseGroup.
    """
    release_group = models.ForeignKey('ReleaseGroup', on_delete=models.CASCADE)
    
    
class RecordingContribution(Contribution):
    """
    Intermediary model for M2M between a Artist and a Recording.
    """
    recording = models.ForeignKey('Recording', on_delete=models.CASCADE)
