import json
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import Profile
from deezerdata.models.deezer_objects import *
from deezerdata.models.deezer_account import *
from musicdata import models
from platform_apis.models import DeezerApiError

from . import data

settings.LOG_RETRIEVAL = False

class ArtistTest(TestCase):
    def setUp(self):
        download_artist = MagicMock(
            return_value=json.loads(data.artist_test_response_text)
        )
        models.Artist.download_data_from_deezer = download_artist
        self.connection_error_artist_patch = patch(
            "musicdata.models.Artist.download_data_from_deezer",
            new=MagicMock(side_effect=ConnectionError()),
        )

    def test_retrieve_from_deezer_existent(self):
        """
        Checks that the retrieval of an existing artist from 
        the Deezer API works.
        """
        artist, created = models.Artist.get_or_retrieve_from_deezer(27)
        self.assertEqual(artist.name, "Daft Punk")
        self.assertEqual(artist.nb_fans_deezer, 3772926)
        self.assertTrue(created)

    def test_retrieve_from_deezer_non_existent(self):
        """
        Checks that the retrieval of an artist with an invalid deezer id
        raises a DeezerApiError.
        """
        download_artist = MagicMock(
            return_value=json.loads(data.inexistant_artist_test_response_text)
        )
        models.Artist.download_data_from_deezer = download_artist
        with self.assertRaises(DeezerApiError):
            artist, created = models.Artist.get_or_retrieve_from_deezer(-1)

    def test_retrieve_from_deezer_no_duplicate(self):
        """
        Checks that the retrieval of an artist already in the database
        does not create a duplicate entry.
        """
        artist, created = models.Artist.get_or_retrieve_from_deezer(27)
        artist, created = models.Artist.get_or_retrieve_from_deezer(27)
        self.assertFalse(created)
        query = models.Artist.objects.all()
        self.assertEqual(len(query), 1)

    def test_retrieve_network_error_during_artist_retrieval(self):
        """
        Tests that if a network error (network unreachable) happens
        during the retrieval of the artist from the Deezer API, no
        corrupted artist is stored in the database.
        See Github issue #24
        """
        self.connection_error_artist_patch.start()
        try:
            track, created = models.Artist.get_or_retrieve_from_deezer(
                27
            )  # Daft Punk
        except ConnectionError:
            pass  # Our mock purposedly raises this error

        with self.assertRaises(models.Artist.DoesNotExist):
            query = models.Artist.objects.get(
                deezer_id=27
            )
        self.connection_error_artist_patch.stop()


class TrackTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user("User", "random@example.com", "pwd")
        profile = Profile.objects.create(user=user)
        user.save()
        profile.save()
        dz_account = DeezerAccount.objects.create(
            profile=profile, user_id=1
        )
        dz_account.save()
        recording = Recording.objects.create(
            isrc="USQX91300108", title="Get Lucky",
        )
        deezer_track = DeezerTrack.objects.create(
            dz_id=67238735,
            title_version="",
            title_short="Get Lucky",
            duration=369,
            readable=True,
            link="https://www.deezer.com/track/67238735",
            share="https://www.deezer.com/track/67238735?utm_source=deezer&utm_content=track-67238735&utm_term=0_1586617186&utm_medium=web",
            rank=809436,
            release_date=dt.date(2013, 5, 17),
            disc_number=1,
            track_number=8,
            explicit_lyrics=False,
            explicit_content_lyrics=0,
            explicit_content_cover=0,
            preview="https://cdns-preview-8.dzcdn.net/stream/c-853d19a12a694ccc74b2501acd802500-3.mp3",
            bpm=116.1,
            gain=-11.3,
        )
        deezer_track.recording = recording
        recording.save()
        deezer_track.save()
        deezer_mp3 = DeezerMp3.objects.create(
            dz_id=-1,
            title="Title",
            artist_name="Artist",
            album_name="Album",
            deezer_account=dz_account
        )
        deezer_mp3.save()
        track3 = Track.objects.create(track_type="")
        track3.save()

    def test_track_str(self):
        """
        Tests the __str__ method of Track.
        """
        track = Track.objects.all()[0]
        self.assertEqual(str(track), "Get Lucky (Deezer)")
        mp3 = Track.objects.all()[1]
        self.assertEqual(str(mp3), "Title (Deezer Mp3)")
        track3 = Track.objects.all()[2]
        self.assertEqual(str(track3), "Track object (3)")