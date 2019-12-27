from django.test import TestCase

from .models import *
from platform_apis.models import DeezerApiError

class ArtistTest(TestCase):
    def test_retrieve_from_deezer_non_existent(self):
        """
        Checks that the retrieval of an artist with an invalid deezer id
        raises a DeezerApiError.
        """
        with self.assertRaises(DeezerApiError):        
            artist, created = Artist.retrieve_from_deezer(-1)
        
