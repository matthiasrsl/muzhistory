from unittest.mock import MagicMock
import json

from django.conf import settings
from django.test import TestCase

import deezerdata.models.deezer_account as deezer_account_models
import deezerdata.models.deezer_objects as deezer_objects_models
import musicdata.models as musicdata_models
from platform_apis.models import DeezerApiError

from . import data


settings.LOG_RETRIEVAL = False


class DeezerAlbumTest(TestCase):
    def setUp(self):
        download_album = MagicMock(
            return_value=json.loads(data.album_test_response_text)
        )
        deezer_objects_models.DeezerAlbum.download_data = download_album

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


class DeezerTrackTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        download_artist = MagicMock(
            return_value=json.loads(data.artist_test_response_text)
        )
        musicdata_models.Artist.download_data_from_deezer = download_artist
        download_album = MagicMock(
            return_value=json.loads(data.album_test_response_text)
        )
        deezer_objects_models.DeezerAlbum.download_data = download_album

    def test_retrieve_existent(self):
        """
        Checks that the retrieval of an existing tracks works.
        """
        download_track = MagicMock(
            return_value=json.loads(data.track_test_response_text)
        )
        deezer_objects_models.DeezerTrack.download_data = download_track

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
        download_track = MagicMock(
            return_value=json.loads(data.track_test_response_text)
        )
        deezer_objects_models.DeezerTrack.download_data = download_track

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
