import json
from unittest.mock import MagicMock
from django.test import TestCase

from musicdata import models
from platform_apis.models import DeezerApiError

from . import data


class ArtistTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        download_artist = MagicMock(
            return_value=json.loads(data.inexistant_artist_test_response_text)
        )
        models.Artist.download_data_from_deezer = download_artist

    def test_retrieve_from_deezer_non_existent(self):
        """
        Checks that the retrieval of an artist with an invalid deezer id
        raises a DeezerApiError.
        """
        with self.assertRaises(DeezerApiError):
            artist, created = models.Artist.get_or_retrieve_from_deezer(-1)
