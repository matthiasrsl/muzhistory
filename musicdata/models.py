from django.db import models

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
    name = models.CharField(max_length=500)
    deezer_id = models.BigIntegerField(null=True, blank=True)
    soptify_id = models.BigIntegerField(null=True, blank=True)
    image_url_deezer_xl = models.URLField(max_length=2000, 
            null=True, blank=True)
    image_url_deezer_large = models.URLField(max_length=2000, 
            null=True, blank=True)
    image_url_deezer_medium = models.URLField(max_length=2000, 
            null=True, blank=True)
    image_url_deezer_small = models.URLField(max_length=2000, 
            null=True, blank=True)
    image_url_spotify_largest = models.URLField(max_length=2000, 
            null=True, blank=True)  # The sizes vary on Spotify.
    image_url_spotify_medium = models.URLField(max_length=2000, 
            null=True, blank=True)
            
    
    def __str__(self):
        return f"{self.name} (Artist)"
        
    def merge(self, artist):
        if self.name != artist.name:
            raise ImpossibleMerge
        else:
            pass  #for rg in self.releasegroup_set.all()
        
        

class ReleaseGroup(models.Model):
    """
    Represents an "album", independently of the medium on which it is released.
    Therefore, it is not platform-dependent.
    Corresponds to a MusicBrainz release group.
    """
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
    barcode_type_choices = [
            ('upc', "UPC"),
            ('none', "No barcode"),
            ('undef', "Undefined"),
    ]
    release_group = models.ForeignKey('ReleaseGroup', on_delete=models.PROTECT)
    barcode = models.CharField(max_length=30, null=True, blank=True)
    barcode_type = models.CharField(max_length=30, 
            choices=barcode_type_choices, default='none')
    release_date = models.DateField()
    
    class Meta:
        abstract = True
        
        
class Recording(models.Model):
    """
    Represents a piece of music, independently of the album (i.e. Release) on
    which it is released. It is therefore not platform-dependent.
    A Recording can be uniquely identified by its ISRC.
    It corresponds to a MusicBrainz's Recording.
    """
    
    isrc = models.CharField(max_length=12)
    title = models.CharField(max_length=1000)
    audio_features = models.TextField(null=True, blank=True)
    audio_analysis = models.TextField(null=True, blank=True)
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
    recording = models.ForeignKey('Recording', on_delete=models.PROTECT)
    
    class Meta:
        abstract = True

    
class Contribution(models.Model):
    """
    Intermediary model for M2M between a Artist and either a Recording or a
    ReleaseGroup.
    """
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
