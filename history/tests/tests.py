from unittest.mock import MagicMock
import json

from django.contrib.auth.models import User
import datetime as dt
from django.test import TestCase

from accounts.models import Profile
import deezerdata.models.deezer_account as deezer_account_models
import deezerdata.models.deezer_objects as deezer_objects_models
from history.models import *
import musicdata.models as musicdata_models

from . import data


from django.conf import settings

settings.LOG_RETRIEVAL = False


class HistoryEntryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user("User", "random@example.com", "pwd")
        profile = Profile.objects.create(user=user)
        user.save()
        profile.save()
        dz_account = deezer_account_models.DeezerAccount.objects.create(
            profile=profile, user_id=1
        )
        dz_account.save()

        download_artist = MagicMock(
            return_value=json.loads(data.artist_test_response_text)
        )
        musicdata_models.Artist.download_data_from_deezer = download_artist
        download_album = MagicMock(
            return_value=json.loads(data.album_test_response_text)
        )
        deezer_objects_models.DeezerAlbum.download_data = download_album
        download_track = MagicMock(
            return_value=json.loads(data.track1_test_response_text)
        )
        deezer_objects_models.DeezerTrack.download_data = download_track

    def setUp(self):
        self.dz_account = deezer_account_models.DeezerAccount.objects.get(
            user_id=1
        )
        self.profile = Profile.objects.get()
        self.entry1_json = json.loads(data.entry1_test_text)
        self.entry2_json = json.loads(data.entry2_test_text)

    def saves_history_correctly(self):
        """
        Checks that HistoryEntry.new_deezer_track_entry correctly saves
        the entry that is passed as a string.
        """
        (
            ignored,
            entry_listening_datetime,
        ) = HistoryEntry.new_deezer_track_entry(self.entry1_json, self.profile)
        self.assertEqual()

    def test_does_not_stores_same_entry_twice(self):
        """
        Checks that if HistoryEntry.new_deezer_track_entry is called a 
        second time with the same timestamp, deezer track id and 
        DeezerAccount than an already stored entry, the entry is not 
        duplicated.
        """
        (
            ignored,
            entry_listening_datetime,
        ) = HistoryEntry.new_deezer_track_entry(self.entry1_json, self.profile)
        self.assertIs(ignored, False)
        self.assertIsInstance(entry_listening_datetime, dt.datetime)
        (
            ignored,
            entry_listening_datetime,
        ) = HistoryEntry.new_deezer_track_entry(self.entry1_json, self.profile)
        self.assertIs(ignored, True)
        self.assertIsInstance(entry_listening_datetime, dt.datetime)

    def test_does_not_ignore_entries_with_same_timestamp(self):
        """
        Checks that if HistoryEntry.new_deezer_track_entry is called a 
        second time with the same timestamp and DeezerAccount but 
        different deezer track id than an already stored entry, the
        entry is not ignored.
        """
        (
            ignored,
            entry_listening_datetime,
        ) = HistoryEntry.new_deezer_track_entry(self.entry1_json, self.profile)
        self.assertIs(ignored, False)
        self.assertIsInstance(entry_listening_datetime, dt.datetime)

        download_track = MagicMock(
            return_value=json.loads(data.track2_test_response_text)
        )
        deezer_objects_models.DeezerTrack.download_data = download_track

        (
            ignored,
            entry_listening_datetime,
        ) = HistoryEntry.new_deezer_track_entry(self.entry2_json, self.profile)
        self.assertIs(ignored, False)
        self.assertIsInstance(entry_listening_datetime, dt.datetime)
