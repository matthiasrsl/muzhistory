from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=500)
    deezer_id = models.BigIntegerField(null=True, blank=True)
    soptify_id = models.BigIntegerField(null=True, blank=True)
    image_url_deezer_xl = models.UrlField(max_length=2000, 
            null=True, blank=True)
    image_url_deezer_large = models.UrlField(max_length=2000, 
            null=True, blank=True)
    image_url_deezer_medium = models.UrlField(max_length=2000, 
            null=True, blank=True)
    image_url_deezer_small = models.UrlField(max_length=2000, 
            null=True, blank=True)
    image_url_spotify_largest = models.UrlField(max_length=2000, 
            null=True, blank=True)  # The sizes vary on Spotify.
    image_url_spotify_medium = models.UrlField(max_length=2000, 
            null=True, blank=True)
    release_groups = models.ManyToManyField(through='ReleaseGroupContribution',
            related_name='contributors')
            
    
    def __str__(self):
        return f"{self.name} (Artist)"
        
    def merge(self, artist):
        pass
        

class ReleaseGroup(models.Model):
    title = models.CharField(max_length=1000)
    album_type = models.CharField(max_length=100)  # Better as ChoiceField ?
    
    def __str__(self):
        return f"{self.title} (Release group)"
        
    def merge(self, release_group):
        pass


class Release(models.Model):
    release_group = models.ForeignKey('ReleaseGroup', on_delete=models.PROTECT)
    barcode = models.CharField(max_length=30)
    barcode_type = models.CharField(max_length=30)
    
    class Meta:
        abstract = True
        
        
class Recording(models.Model):
    isrc = models.CharField(max_length=12)
    title = models.CharField(max_length=1000)
    audio_features = models.JSONField()
    

    
class Contribution(models.ModelField):
    role = models.CharField(max_length=20)
    
    class Meta:
        abstract = True

        
class ReleaseGroupContribution(Contribution):
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    release_group = models.ForeignKey('ReleaseGroup', on_delete=models.CASCADE)
