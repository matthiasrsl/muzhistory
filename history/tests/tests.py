from unittest.mock import MagicMock, patch
import json

from django.contrib.auth.models import User
import datetime as dt
from django.test import TestCase

from requests.exceptions import ConnectionError

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

    def setUp(self):
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
        self.dz_account = deezer_account_models.DeezerAccount.objects.get(
            user_id=1
        )
        self.profile = Profile.objects.get()
        self.deezer_account = deezer_account_models.DeezerAccount.objects.get()
        self.entry1_json = json.loads(data.entry1_test_text)
        self.entry2_json = json.loads(data.entry2_test_text)
        mp3_data = json.loads(data.mp3_test_response_text)
        self.download_mp3_data_patch = patch(
            "deezerdata.models.deezer_objects.DeezerMp3.download_data",
            new=MagicMock(return_value=mp3_data),
        )

    def test_saves_deezer_track_history_entry_correctly(self):
        """
        Checks that HistoryEntry.new_deezer_track_entry correctly saves
        the entry that is passed as a string.
        """
        (
            ignored,
            entry_listening_datetime,
        ) = HistoryEntry.new_deezer_track_entry(
            self.entry1_json, self.profile, self.deezer_account
        )
        entry = HistoryEntry.objects.all().order_by("-id")[0]
        self.assertEqual(entry.profile, self.profile)
        self.assertEqual(entry.deezer_account, self.deezer_account)
        self.assertEqual(entry.track.recording.title, "Get Lucky")
        self.assertEqual(
            entry.entry_type,
            HistoryEntry.SpecialHistoryEntryChoices.LISTENING.value,
        )

    def test_saves_deezer_mp3_history_entry_correctly(self):
        """
        Tests the retrieval of a Deezer HistoryEntry with
        a DeezerMp3.
        """
        self.download_mp3_data_patch.start()
        self.entry_mp3 = json.loads(data.entry_deezer_mp3_response_text)
        (
            ignored,
            entry_listening_datetime,
        ) = HistoryEntry.new_deezer_track_entry(
            self.entry_mp3, self.profile, self.deezer_account
        )
        entry = HistoryEntry.objects.all().order_by("-id")[0]
        self.assertEqual(entry.track.recording.title, "La Noyée")
        self.assertEqual(
            entry.track.deezertrack.deezermp3.artist_name, "Serge Gainsbourg"
        )
        self.download_mp3_data_patch.stop()

    def test_does_not_stores_same_deezer_track_entry_twice(self):
        """
        Checks that if HistoryEntry.new_deezer_track_entry is called a 
        second time with the same timestamp, deezer track id and 
        DeezerAccount than an already stored entry, the entry is not 
        duplicated.
        """
        (
            ignored,
            entry_listening_datetime,
        ) = HistoryEntry.new_deezer_track_entry(
            self.entry1_json, self.profile, self.deezer_account
        )
        self.assertIs(ignored, False)
        self.assertIsInstance(entry_listening_datetime, dt.datetime)
        (
            ignored,
            entry_listening_datetime,
        ) = HistoryEntry.new_deezer_track_entry(
            self.entry1_json, self.profile, self.deezer_account
        )
        self.assertIs(ignored, True)
        self.assertIsInstance(entry_listening_datetime, dt.datetime)

    def test_does_not_ignore_deezer_track_entries_with_same_timestamp(self):
        """
        Checks that if HistoryEntry.new_deezer_track_entry is called a 
        second time with the same timestamp and DeezerAccount but 
        different deezer track id than an already stored entry, the
        entry is not ignored.
        """
        (
            ignored,
            entry_listening_datetime,
        ) = HistoryEntry.new_deezer_track_entry(
            self.entry1_json, self.profile, self.deezer_account
        )
        self.assertIs(ignored, False)
        self.assertIsInstance(entry_listening_datetime, dt.datetime)

        download_track = MagicMock(
            return_value=json.loads(data.track2_test_response_text)
        )
        deezer_objects_models.DeezerTrack.download_data = download_track

        (
            ignored,
            entry_listening_datetime,
        ) = HistoryEntry.new_deezer_track_entry(
            self.entry2_json, self.profile, self.deezer_account
        )
        self.assertIs(ignored, False)
        self.assertIsInstance(entry_listening_datetime, dt.datetime)

    def test_retrieve_network_error_during_artist_retrieval(self):
        """
        Tests that if a network error (network unreachable) happens
        during the retrieval of a contributor, no corrupted entry
        is stored in the database and the profile last_history_request is not changed.
        """
        download_artist = MagicMock(side_effect=ConnectionError())
        musicdata_models.Artist.download_data_from_deezer = download_artist
        try:
            (
                ignored,
                entry_listening_datetime,
            ) = HistoryEntry.new_deezer_track_entry(
                self.entry2_json, self.profile, self.deezer_account
            )
        except ConnectionError:
            pass  # Our mock purposedly raises this error

        with self.assertRaises(HistoryEntry.DoesNotExist):
            query = HistoryEntry.objects.get()
