import datetime as dt
import json

from django.conf import settings
from django.db import models
from django.utils import timezone as tz

from history.models import HistoryEntry
from musicdata.models import *
from platform_apis.models import *
from tools.models import log_exceptions


class DeezerAccount(PlatformAccount):
    """
    A user account on Deezer.
    """

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

    @log_exceptions
    def update(self):
        url = settings.DEEZER_API_USER_URL
        params = {"access_token": self.access_token}
        response = requests.get(url, params=params)
        r_data = response.json()

        try:
            error_type = r_data["error"]["type"]
            message = r_data["error"]["message"]
            code = r_data["error"]["code"]
            raise DeezerApiError(error_type, message, code)
        except KeyError:
            pass  # No API-related error occured.

        self.user_id = r_data["id"]
        self.name = r_data["name"]
        self.lastname = r_data["lastname"]
        self.firstname = r_data["firstname"]
        self.email = r_data["email"]
        self.status = r_data["status"]
        if r_data["birthday"] != "0000-00-00":
            birthday_list = r_data["birthday"].split("-")
            birthday_list = [int(elt) for elt in birthday_list]
            self.birthday = dt.date(*birthday_list)
        inscription_date_list = r_data["inscription_date"].split("-")
        inscription_date_list = [int(elt) for elt in inscription_date_list]
        self.inscription_date = dt.date(*inscription_date_list)
        self.gender = r_data["gender"]
        self.link = r_data["link"]
        self.picture_small = r_data["picture_small"]
        self.picture_medium = r_data["picture_medium"]
        self.picture_big = r_data["picture_big"]
        self.picture_xl = r_data["picture_xl"]
        market, created = Market.objects.get_or_create(code=r_data["country"])
        market.save()
        self.market = market
        self.lang = r_data["lang"]
        self.is_kid = r_data["is_kid"]
        self.explicit_content_level = r_data["explicit_content_level"]
        self.flow_url = r_data["tracklist"]

    def download_history_data(self, url):  # pragma: no cover
        """
        Downloads the account's listening history data from the Deezer Api.
        """
        if url:
            api_request = requests.get(url)
        else:
            api_request = requests.get(
                settings.DEEZER_API_HISTORY_URL.format(self.user_id),
                params={"access_token": self.access_token,},
            )
        return api_request.json()

    def retrieve_history_iteration(self, url=None):
        """
        Makes a request to the Deezer API for a segment of a user's
        listening history, and creates the entries.
        """
        api_response = self.download_history_data(url)
        #print(api_response)
        history_json = api_response["data"]
        try:
            next_url = api_response["next"]
        except KeyError:
            next_url = ""

        for entry_json in history_json:
            # We create the new entry if necessary and if not, increment the
            # counter
            # The entries are in the json response in reverse
            # chronological order.
            (
                ignored,
                oldest_listening_datetime,
            ) = HistoryEntry.new_deezer_track_entry(entry_json, self.profile)

        return (next_url, oldest_listening_datetime)

    @log_exceptions
    def retrieve_history(self):
        """
        Retrieves the listening history of a user from the Deezer API.
        """
        (
            next_url,
            oldest_listening_datetime,
        ) = self.retrieve_history_iteration()
        while next_url:
            (
                next_url,
                oldest_listening_datetime,
            ) = self.retrieve_history_iteration(next_url)

        if oldest_listening_datetime > self.last_history_request:
            """ellipsis_entry = HistoryEntry(
                profile=self,
                listening_datetime=oldest_listening_datetime,
                entry_type="history_ellipsis",
            )
            ellipsis_entry.save()"""
            pass

        self.last_history_request = tz.now()
        self.save()
