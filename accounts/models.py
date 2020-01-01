from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone as tz
from django.conf import settings

class Profile(models.Model):
    """
    Extension of the User model.
    """
    version = models.IntegerField(default=settings.MH_VERSION)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    track_location = models.BooleanField(default=False)
    


class PlatformAccount(models.Model):
    """
    A user account on a music streaming platform.
    """
    version = models.IntegerField(default=settings.MH_VERSION)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    user_id = models.CharField(max_length=100)
    access_token = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField()
    market = models.ForeignKey('platform_apis.Market', on_delete=models.PROTECT,
            null=True, blank=True)
    last_history_request = models.DateTimeField(null=True, blank=True,
            default=settings.OLDEST_DATE)
    name = models.CharField(max_length=300)
    link = models.URLField(max_length=2000)
    
    class Meta:
        abstract = True
    
    
class DeezerAccount(PlatformAccount):
    version = models.IntegerField(default=settings.MH_VERSION)
    lastname = models.CharField(max_length=300)
    firstname = models.CharField(max_length=300)
    status = models.IntegerField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    inscription_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1)
    link = models.URLField(max_length=2000)
    picture_small = models.URLField(max_length=2000)
    picture_medium = models.URLField(max_length=2000)
    picture_big = models.URLField(max_length=2000)
    picture_xl = models.URLField(max_length=2000)
    lang = models.CharField(max_length=2)
    is_kid = models.BooleanField(null=True)
    explicit_content_level = models.CharField(max_length=100)
    flow_url = models.URLField(max_length=2000)
    
    
