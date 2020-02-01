import datetime as dt

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone as tz
from django.conf import settings

import requests

from platform_apis.models import DeezerOAuthError, Market

class Profile(models.Model):
    """
    Extension of the User model.
    """
    version = models.IntegerField(default=settings.MH_VERSION)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    track_location = models.BooleanField(default=False)
    
    def get_deezer_access_token(self, code):
        """
        Retrieves the user's access token from Deezer after authentication.
        """
        url = settings.DEEZER_ACCESS_TOKEN_URL
        params = {
                'app_id': settings.DEEZER_API_APP_ID,
                'secret': settings.DEEZER_API_SECRET_KEY,
                'code': code,
                'output': 'json',
        }
        response = requests.get(url, params=params)
        
        if response.status_code != 200 or response.text == 'wrong code':
            raise DeezerOAuthError(response.text)
        else:
            response_data = response.json()
            deezer_account = DeezerAccount.objects.create(
                    profile=self,
                    access_token=response_data['access_token'],
            )
            deezer_account.save()
                    


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
    """
    A user account on Deezer.
    """
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
    
    def update(self):
        url = settings.DEEZER_API_USER_URL
        params = {'access_token': self.access_token}
        response = requests.get(url, params=params)
        r_data = response.json()
        
        try:
            error_type = r_data['error']['type']
            message = r_data['error']['message']
            code = r_data['error']['code']
            raise DeezerApiError(error_type, message, code)
        except KeyError:
            pass  # No API-related error occured.
            
        self.user_id = r_data['id']
        self.name = r_data['name']
        self.lastname = r_data['lastname']
        self.firstname = r_data['firstname']
        self.email = r_data['email']
        self.status = r_data['status']
        if r_data['birthday'] != "0000-00-00":
            birthday_list = r_data['birthday'].split('-')
            birthday_list = [int(elt) for elt in birthday_list]
            self.birthday = dt.date(*birthday_list)
        inscription_date_list = r_data['inscription_date'].split('-')
        inscription_date_list = [int(elt) for elt in inscription_date_list]
        self.inscription_date = dt.date(*inscription_date_list)
        self.gender = r_data['gender']
        self.link = r_data['link']
        self.picture_small = r_data['picture_small']
        self.picture_medium = r_data['picture_medium']
        self.picture_big = r_data['picture_big']
        self.picture_xl = r_data['picture_xl']
        market, created = Market.objects.get_or_create(code=r_data['country'])
        market.save()
        self.market = market
        self.lang = r_data['lang']
        self.is_kid = r_data['is_kid']
        self.explicit_content_level = r_data['explicit_content_level']
        self.flow_url = r_data['tracklist']
        
    
