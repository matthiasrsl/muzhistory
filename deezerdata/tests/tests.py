import json
import datetime as dt
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone as tz

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

    def test_genre(self):
        """
        Tests that during the etrieval of a DeezerAlbum, its genres are specified in its ReleaseGroup.
        """
        album, created = deezer_objects_models.DeezerAlbum.get_or_retrieve(
            6575789
        )  # Daft Punk's Random Access Memories
        self.assertEqual(album.release_group.genres.all()[0].name, "Pop")
        self.assertEqual(album.release_group.genres.all()[0].dz_id, 132)

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
        Checks that the retrieval of an existing track works.
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
        (Deezer Mp3 have their own retrieval method).
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
            new=MagicMock(side_effect=[history1, history2]),
        )
        self.download_history_data_patch.start()

    def tearDown(self):
        self.download_history_data_patch.stop()
        try:
            self.connection_error_patch.stop()
        except RuntimeError:
            pass  #  The patch has been stopped in a test that didn't need it.

    def test_retrieve_history_normal_case(self):
        """
        Tests that DeezerAccount.retrieve_history works in
        normal conditions.
        """
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
        self.connection_error_patch.start()
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
        self.connection_error_patch.stop()

    def test_ellipsis_entry_if_last_update_too_old(self):
        """
        Tests that if the last_history_request attribute of the profile
        is older that the oldest entry in the data retrieved, an 
        ellispsis history entry is created.
        """
        deezer_account = deezer_account_models.DeezerAccount.objects.get()
        deezer_account.last_history_request = tz.make_aware(
            dt.datetime(year=2020, month=1, day=1), tz.get_current_timezone()
        )
        deezer_account.save()
        deezer_account.retrieve_history()
        entries = HistoryEntry.objects.filter(
            entry_type=HistoryEntry.SpecialHistoryEntryChoices.DEEZER_ELLIPSIS
        )
        self.assertEqual(entries.count(), 1)


class DeezerMp3Test(TestCase):
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
        self.deezer_account = deezer_account_models.DeezerAccount.objects.get()
        history1 = json.loads(data.history1_test_data_text)
        history2 = json.loads(data.history2_test_data_text)
        mp3_data = json.loads(data.mp3_test_response_text)
        inexistant_response = json.loads(data.inexistant_track_response_text)
        unauthorized_response = json.loads(data.mp3_unauthorized_response_text)
        negative_id_reponse = json.loads(data.track_negative_id_response_test)
        self.download_history_data_patch = patch(
            "deezerdata.models.deezer_account.DeezerAccount.download_history_data",
            new=MagicMock(side_effect=[history1, history2]),
        )
        self.download_mp3_data_patch = patch(
            "deezerdata.models.deezer_objects.DeezerMp3.download_data",
            new=MagicMock(return_value=mp3_data),
        )
        self.download_inexistant_patch = patch(
            "deezerdata.models.deezer_objects.DeezerMp3.download_data",
            new=MagicMock(return_value=inexistant_response),
        )
        self.download_unauthorized_patch = patch(
            "deezerdata.models.deezer_objects.DeezerMp3.download_data",
            new=MagicMock(return_value=unauthorized_response),
        )
        self.download_negative_id_track_patch = patch(
            "deezerdata.models.deezer_objects.DeezerMp3.download_data",
            new=MagicMock(return_value=negative_id_reponse),
        )

    def test_retrieve_history_check_mp3_account(self):
        """
        Tests that the deezer_account of a DeezerMp3 is filled
        during a history retrieval.
        """
        self.download_history_data_patch.start()
        self.deezer_account = deezer_account_models.DeezerAccount.objects.get()
        self.deezer_account.retrieve_history()
        deezer_mp3 = deezer_objects_models.DeezerMp3.objects.get()
        self.assertEqual(deezer_mp3.deezer_account, self.deezer_account)
        self.download_history_data_patch.stop()

    def test_retrieve_existing(self):
        """
        Checks that the retrieval of an existing mp3 works.
        """
        self.download_mp3_data_patch.start()
        deezer_objects_models.DeezerMp3.get_or_retrieve(
            -2902124464, self.deezer_account
        )
        query = deezer_objects_models.DeezerMp3.objects.filter(
            dz_id=-2902124464
        )
        self.assertEqual(query.count(), 1)
        self.assertEqual(query[0].deezer_account, self.deezer_account)
        self.download_mp3_data_patch.stop()

    def test_retrieve_nonexistent(self):
        """
        Tests that the retrieval of a mp3 with an invalid deezer id
        raises a DeezerApiError.
        """
        self.download_inexistant_patch.start()
        with self.assertRaises(DeezerApiError):
            track, created = deezer_objects_models.DeezerMp3.get_or_retrieve(
                -65426, self.deezer_account
            )
        with self.assertRaises(deezer_objects_models.DeezerMp3.DoesNotExist):
            query = deezer_objects_models.DeezerMp3.objects.get()
        self.download_inexistant_patch.stop()

    def test_retrieve_unauthorized(self):
        """
        Tests that the retrieval of a mp3 with the wrong access
        token raises a DeezerApiError and does not leave a blank
        mp3 in the database.
        """
        self.download_unauthorized_patch.start()
        with self.assertRaises(DeezerApiError):
            tuple_ = deezer_objects_models.DeezerMp3.get_or_retrieve(
                -2902124464, self.deezer_account
            )
        with self.assertRaises(deezer_objects_models.DeezerMp3.DoesNotExist):
            query = deezer_objects_models.DeezerMp3.objects.get()
        self.download_unauthorized_patch.stop()

    def test_retrieve_no_mp3(self):
        """
        Some tracks with a negative deezer_id in the Deezer database are
        not user mp3s but unavailable tracks. This test tests that 
        if such a track is attempted to be retrieved via the DeezerMp3
        model, a ValueError is raised and no blank mp3 is stored.
        """
        self.download_negative_id_track_patch.start()
        with self.assertRaises(ValueError):
            tuple_ = deezer_objects_models.DeezerMp3.get_or_retrieve(
                -64642681, self.deezer_account
            )
        with self.assertRaises(deezer_objects_models.DeezerMp3.DoesNotExist):
            query = deezer_objects_models.DeezerMp3.objects.get()
        self.download_negative_id_track_patch.stop()

    def test_retrieve_regular_track(self):
        """
        Tests that trying to retrieve a regular track raises an 
        exception (DeezerTracks have their own retrieval method).
        """
        with self.assertRaises(ValueError):
            mp3, created = deezer_objects_models.DeezerMp3.get_or_retrieve(
                67238735, self.deezer_account
            )
        with self.assertRaises(deezer_objects_models.DeezerMp3.DoesNotExist):
            query = deezer_objects_models.DeezerMp3.objects.get()
