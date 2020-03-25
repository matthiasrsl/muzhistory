import datetime as dt

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import models
from django.utils import timezone as tz

import requests
from deezerdata.models import *
from platform_apis.models import (DeezerOAuthError, DeezerRefusedAccessError,
                                  Market)


class Profile(models.Model):
    """
    Extension of the User model.
    """
    version = models.IntegerField(default=settings.MH_VERSION)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    track_location = models.BooleanField(default=False)
    last_history_request = models.DateTimeField(null=True, blank=True,
            default=settings.OLDEST_DATE)
    

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

        response.raise_for_status()

        if response.text == 'wrong code':
            raise DeezerOAuthError(response.text)
        else:
            response_data = response.json()

            if 'access_token' in response_data:
                return response_data['access_token']
            elif 'error_reason' in response_data:
                if response_data['error_reason'] == 'user_denied':
                    raise DeezerRefusedAccessError()
                else:
                    raise DeezerOAuthError(response_data['error_reason'])
            else:
                raise DeezerOAuthError("Unknown error.")

    def add_deezer_account(self, access_token):
        # We retrieve the Deezer user id to check if it is already
        # in the database.
        url_deezer_user = settings.DEEZER_API_USER_URL
        params_deezer_user = {
            'access_token': access_token
        }
        response_deezer_user = requests.get(url_deezer_user,
                                            params=params_deezer_user)
        r_data_deezer_user = response_deezer_user.json()

        try:
            error_type = r_data_deezer_user['error']['type']
            message = r_data_deezer_user['error']['message']
            code = r_data_deezer_user['error']['code']
            raise DeezerApiError(error_type, message, code)
        except KeyError:
            pass  # No API-related error occured.

        deezer_user_id = r_data_deezer_user['id']

        deezer_account, created = DeezerAccount.objects.get_or_create(
            user_id=deezer_user_id,
        )

        if created:
            deezer_account.profile = self
        else:
            if deezer_account.profile != self:
                raise PermissionDenied

        deezer_account.access_token = access_token
        deezer_account.update()
        deezer_account.save()
