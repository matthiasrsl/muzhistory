from django.conf import settings
from django.test import TestCase

from deezerdata.models.deezer_account import *
from deezerdata.models.deezer_objects import *
from musicdata.models import *
from platform_apis.models import DeezerApiError

settings.LOG_RETRIEVAL = False


class DeezerAlbumTest(TestCase):
    def test_retrieve_non_existent(self):
        """
        Checks that the retrieval of an album with an invalid deezer id
        raises a DeezerApiError.
        """
        with self.assertRaises(DeezerApiError):
            album, created = DeezerAlbum.get_or_retrieve(-1)


class DeezerTrackTest(TestCase):
    """@classmethod
    def setUpTestData(self):"""
        

    def test_retrieve_existent(self):
        """
        Checks that the retrieval of an existing tracks works.
        """
        track, created = DeezerTrack.get_or_retrieve(67238735)  # Get Lucky
        query_tracks = DeezerTrack.objects.filter(dz_id=67238735)
        query_albums = DeezerAlbum.objects.filter(dz_id=6575789)
        query_artists = Artist.objects.filter(deezer_id=27)
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
        track, created = DeezerTrack.get_or_retrieve(67238735)  # Get Lucky
        track, created = DeezerTrack.get_or_retrieve(67238735)
        query_tracks = DeezerTrack.objects.filter(dz_id=67238735)
        self.assertEqual(len(query_tracks), 1)

    def test_retrieve_non_existent(self):
        """
        Checks that the retrieval of an track with an invalid deezer id
        raises a DeezerApiError.
        """
        with self.assertRaises(DeezerApiError):
            track, created = DeezerTrack.get_or_retrieve(0)

    def test_retrieve_not_authorized(self):
        """
        Checks that the retrieval of a user mp3 without oauth authentication
        raises a DeezerApiError.
        """
        with self.assertRaises(DeezerApiError):
            track, created = DeezerTrack.get_or_retrieve(-2834538522)
