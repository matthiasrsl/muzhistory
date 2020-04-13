from unittest.mock import MagicMock, patch
import json

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User

from requests.exceptions import ConnectionError

from accounts.models import Profile
import deezerdata.models.deezer_account as deezer_account_models
import deezerdata.models.deezer_objects as deezer_objects_models
from history.models import HistoryEntry
import musicdata.models as musicdata_models
from platform_apis.models import DeezerApiError

from . import data


settings.LOG_RETRIEVAL = False


class DeezerAlbumTest(TestCase):
    def setUp(self):
        download_artist = MagicMock(
            return_value=json.loads(data.artist_test_response_text)
        )
        download_album = MagicMock(
            return_value=json.loads(data.album_test_response_text)
        )
        deezer_objects_models.DeezerAlbum.download_data = download_album

        self.connection_error_artist_patch = patch(
            "musicdata.models.Artist.download_data_from_deezer",
            new=MagicMock(side_effect=ConnectionError()),
        )
        self.connection_error_album_patch = patch(
            "deezerdata.models.deezer_objects.DeezerAlbum.download_data",
            new=MagicMock(side_effect=ConnectionError()),
        )

    def test_retrieve_existent(self):
        """
        Checks that the retrieval of an existing album from 
        the Deezer API works.
        """
        (album, created,) = deezer_objects_models.DeezerAlbum.get_or_retrieve(
            6575789
        )
        self.assertEqual(album.release_group.title, "Random Access Memories")
        self.assertEqual(album.nb_tracks, 13)
        self.assertTrue(created)

    def test_retrieve_non_existent(self):
        """
        Checks that the retrieval of an album with an invalid deezer id
        raises a DeezerApiError.
        """
        download_album = MagicMock(
            return_value=json.loads(data.inexistant_album_response_text)
        )
        deezer_objects_models.DeezerAlbum.download_data = download_album
        with self.assertRaises(DeezerApiError):
            album, created = deezer_objects_models.DeezerAlbum.get_or_retrieve(
                -1
            )

    def test_retrieve_no_duplicate(self):
        """
        Checks that the retrieval of an album already in the database
        does not create a duplicate entry.
        """
        (album, created,) = deezer_objects_models.DeezerAlbum.get_or_retrieve(
            6575789
        )
        (album, created,) = deezer_objects_models.DeezerAlbum.get_or_retrieve(
            6575789
        )
        self.assertFalse(created)
        query = deezer_objects_models.DeezerAlbum.objects.all()
        self.assertEqual(len(query), 1)

    def test_retrieve_network_error_during_artist_retrieval(self):
        """
        Tests that if a network error (network unreachable) happens
        during the retrieval of a contributor, no corrupted album
        is stored in the database.
        """
        self.connection_error_artist_patch.start()
        try:
            album, created = deezer_objects_models.DeezerAlbum.get_or_retrieve(
                6575789
            )  # Daft Punk's Random Access Memories
        except ConnectionError:
            pass  # Our mock purposedly raises this error

        with self.assertRaises(deezer_objects_models.DeezerAlbum.DoesNotExist):
            query = deezer_objects_models.DeezerAlbum.objects.get(
                dz_id=6575789
            )
        self.connection_error_artist_patch.stop()

    def test_retrieve_network_error_during_album_retrieval(self):
        """
        Tests that if a network error (network unreachable) happens
        during the retrieval of the album - and not a linked object,
        but the track himself - no corrupted album
        is stored in the database.
        See Github issue #24
        """
        self.connection_error_album_patch.start()
        try:
            album, created = deezer_objects_models.DeezerAlbum.get_or_retrieve(
                6575789
            )  # Daft Punk's Random Access Memories
        except ConnectionError:
            pass  # Our mock purposedly raises this error

        with self.assertRaises(deezer_objects_models.DeezerAlbum.DoesNotExist):
            query = deezer_objects_models.DeezerAlbum.objects.get(
                dz_id=6575789
            )
        self.connection_error_album_patch.stop()


class DeezerTrackTest(TestCase):
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
            return_value=json.loads(data.track_test_response_text)
        )
        deezer_objects_models.DeezerTrack.download_data = download_track

    def test_retrieve_existent(self):
        """
        Checks that the retrieval of an existing tracks works.
        """
        track, created = deezer_objects_models.DeezerTrack.get_or_retrieve(
            67238735
        )  # Get Lucky
        query_tracks = deezer_objects_models.DeezerTrack.objects.filter(
            dz_id=67238735
        )
        query_albums = deezer_objects_models.DeezerAlbum.objects.filter(
            dz_id=6575789
        )
        query_artists = musicdata_models.Artist.objects.filter(deezer_id=27)
        self.assertEqual(len(query_tracks), 1)
        self.assertEqual(len(query_albums), 1)
        self.assertEqual(len(query_artists), 1)
        self.assertEqual(track.recording.title, "Get Lucky")
        self.assertEqual(
            track.release.release_group.title, "Random Access Memories"
        )
        self.assertEqual(
            track.release.release_group.contributors.all()[0].name, "Daft Punk"
        )

    def test_retrieve_no_duplicate(self):
        """
        Checks that the retrieval of a track already in the database
        does not create a duplicate entry.
        """
        track, created = deezer_objects_models.DeezerTrack.get_or_retrieve(
            67238735
        )  # Get Lucky
        track, created = deezer_objects_models.DeezerTrack.get_or_retrieve(
            67238735
        )
        query_tracks = deezer_objects_models.DeezerTrack.objects.filter(
            dz_id=67238735
        )
        self.assertEqual(len(query_tracks), 1)

    def test_retrieve_non_existent(self):
        """
        Checks that the retrieval of an track with an invalid deezer id
        raises a DeezerApiError.
        """
        download_track = MagicMock(
            return_value=json.loads(data.inexistant_track_response_text)
        )
        deezer_objects_models.DeezerTrack.download_data = download_track

        with self.assertRaises(DeezerApiError):
            track, created = deezer_objects_models.DeezerTrack.get_or_retrieve(
                0
            )

    def test_retrieve_mp3(self):
        """
        Tests that trying to retrieve a DeezerMp3 raises an exception.
        (Deezer Mp3 are retrievable from the api, and it would be 
        useless as all relevant information is obtained during 
        the history iteration retrieval).
        """
        download_track = MagicMock(
            return_value=json.loads(data.mp3_test_response_text)
        )
        deezer_objects_models.DeezerTrack.download_data = download_track
        with self.assertRaises(ValueError):
            track, created = deezer_objects_models.DeezerTrack.get_or_retrieve(
                -2834538522
            )

    def test_retrieve_network_error_during_artist_retrieval(self):
        """
        Tests that if a network error (network unreachable) happens
        during the retrieval of a contributor, no corrupted track
        is stored in the database.
        """
        download_artist = MagicMock(side_effect=ConnectionError())
        musicdata_models.Artist.download_data_from_deezer = download_artist

        try:
            track, created = deezer_objects_models.DeezerTrack.get_or_retrieve(
                67238735
            )  # Get Lucky
        except ConnectionError:
            pass  # Our mock purposedly raises this error

        with self.assertRaises(deezer_objects_models.DeezerTrack.DoesNotExist):
            query = deezer_objects_models.DeezerTrack.objects.get(
                dz_id=67238735
            )

    def test_retrieve_network_error_during_track_retrieval(self):
        """
        Tests that if a network error (network unreachable) happens
        during the retrieval of the track - and not a linked object,
        but the track himself - no corrupted track
        is stored in the database.
        See Github issue #24
        """
        download_track = MagicMock(side_effect=ConnectionError())
        deezer_objects_models.DeezerTrack.download_data = download_track

        try:
            track, created = deezer_objects_models.DeezerTrack.get_or_retrieve(
                67238735
            )  # Get Lucky
        except ConnectionError:
            pass  # Our mock purposedly raises this error

        with self.assertRaises(deezer_objects_models.DeezerTrack.DoesNotExist):
            query = deezer_objects_models.DeezerTrack.objects.get(
                dz_id=67238735
            )


class DeezerAccountTest(TestCase):
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
        self.dz_account = deezer_account_models.DeezerAccount.objects.get()
        
        download_artist = MagicMock(
            return_value=json.loads(data.artist_test_response_text)
        )
        musicdata_models.Artist.download_data_from_deezer = download_artist
        download_album = MagicMock(
            return_value=json.loads(data.album_test_response_text)
        )
        deezer_objects_models.DeezerAlbum.download_data = download_album
        download_track = MagicMock(
            return_value=json.loads(data.track_test_response_text)
        )
        deezer_objects_models.DeezerTrack.download_data = download_track

        self.connection_error_patch = patch(
            "musicdata.models.Artist.download_data_from_deezer",
            new=MagicMock(side_effect=ConnectionError()),
        )
        history1 = json.loads(data.history1_test_data_text)
        history2 = json.loads(data.history2_test_data_text)
        self.download_history_data_patch = patch(
            "deezerdata.models.deezer_account.DeezerAccount.download_history_data",
            new=MagicMock(
                side_effect=[history1, history2]
            ),
        )
        self.download_history_data_patch.start()
        self.connection_error_patch.start()
        

    def tearDown(self):
        self.download_history_data_patch.stop()
        try:
            self.connection_error_patch.stop()
        except RuntimeError:
            pass  # The patch has been stopped in a test that didn't need it.

    def test_retrieve_history_normal_case(self):
        """
        Tests that DeezerAccount.retrieve_history works in
        normal conditions.
        """
        self.connection_error_patch.stop()
        original_datetime = (
            self.dz_account.last_history_request
        )  # Sould be the Epoch.
        self.dz_account.retrieve_history()
        self.assertNotEqual(
            self.dz_account.last_history_request, original_datetime
        )
        query = HistoryEntry.objects.filter(timestamp=1586441751)
        self.assertEqual(len(query), 1)
        
    def test_retrieve_history_network_error(self):
        """
        Tests that the account last_history_request is not updated
        if a network error (network unreachable) occurs during
        the retrieval process.
        """
        original_datetime = (
            self.dz_account.last_history_request
        )  # Sould be the Epoch.
        try:
            self.dz_account.retrieve_history()
        except ConnectionError:
            pass  # Our mock purposedly raises this error
        self.assertEqual(
            self.dz_account.last_history_request, original_datetime
        )
        
