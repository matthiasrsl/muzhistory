from json import loads

from django.contrib.auth.models import User
import datetime as dt
from django.test import TestCase

from accounts.models import Profile
from deezerdata.models import DeezerAccount

from .models import *

from django.conf import settings

settings.LOG_RETRIEVAL = False

class HistoryEntryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user("User", "random@example.com", "pwd")
        profile = Profile.objects.create(user=user)
        user.save()
        profile.save()
        dz_account = DeezerAccount.objects.create(profile=profile, user_id=1)
        dz_account.save()

    def setUp(self):
        self.dz_account = DeezerAccount.objects.get(user_id=1)
        self.profile = Profile.objects.get()

    def test_does_not_stores_same_entry_twice(self):
        """
        Checks that if HistoryEntry.new_deezer_track_entry is called a second
        with the same timestamp and DeezerAccount than an already stored
        entry, the entry is not duplicated.
        """
        entry_json = loads(
            """{
            "id":3464227,"readable":true,
            "title":"Radio Varsavia (Remastered)",
            "title_short":"Radio Varsavia","title_version":"(Remastered)",
            "link":"https://www.deezer.com/track/3464227",
            "duration":253,"rank":465054,"explicit_lyrics":false,
            "explicit_content_lyrics":0,"explicit_content_cover":0,
            "preview": "https://example.com/c.mp3","timestamp":1585147676,
            "artist":{
                "id":2850,"name":"Franco Battiato",
                "link":"https://www.deezer.com/artist/2850",
                "tracklist":"https://api.deezer.com","type":"artist"
            },
            "album":{
                "id":328643,
                "title":"L'Arca Di No (2008 Remastered Edition)",
                "link":"https://www.deezer.com/album/328643",
                "cover":"https://api.deezer.com/album/328643/image",
                "cover_small":"https://i.imgur.com/nszu54A.jpg",
                "cover_medium":"https://i.imgur.com/nszu54A.jpg",
                "cover_big":"https://i.imgur.com/nszu54A.jpg",
                "cover_xl":"https://i.imgur.com/nszu54A.jpg",
                "tracklist":"https://api.deezer.com/album/328643/tracks",
                "type":"album"
            },
            "type":"track"}"""
        )
        (
            ignored,
            entry_listening_datetime,
        ) = HistoryEntry.new_deezer_track_entry(entry_json, self.profile)
        self.assertIs(ignored, False)
        self.assertIsInstance(entry_listening_datetime, dt.datetime)
        (
            ignored,
            entry_listening_datetime,
        ) = HistoryEntry.new_deezer_track_entry(entry_json, self.profile)
        self.assertIs(ignored, True)
        self.assertIsInstance(entry_listening_datetime, dt.datetime)
