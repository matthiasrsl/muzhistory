from django.test import TestCase

from platform_apis.models import DeezerApiError

from .models import *


class DeezerAlbumTest(TestCase):
    def test_retrieve_non_existent(self):
        """
        Checks that the retrieval of an album with an invalid deezer id
        raises a DeezerApiError.
        """
        with self.assertRaises(DeezerApiError):
            album, created = DeezerAlbum.retrieve(-1)


class DeezerTrackTest(TestCase):
    def test_retrieve_non_existent(self):
        """
        Checks that the retrieval of an track with an invalid deezer id
        raises a DeezerApiError.
        """
        with self.assertRaises(DeezerApiError):
            track, created = DeezerTrack.retrieve(0)

    def test_retrieve_not_authorized(self):
        """
        Checks that the retrieval of a user mp3 without oauth authentication
        raises a DeezerApiError.
        """
        with self.assertRaises(DeezerApiError):
            track, created = DeezerTrack.retrieve(-2834538522)
