from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render

from requests.exceptions import RequestException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from platform_apis.models import DeezerOAuthError
from deezerdata.models.deezer_account import DeezerAccount

from musicdata.models import Artist, ReleaseGroup, Release, Recording, Track
from api.serializers.musicdata import (
    ArtistSerializer,
    ReleaseGroupSerializer,
    RecordingSerializer,
    TrackSerializer,
)


class ArtistAPI(APIView):
    """
    View to get information about an artist.

    This view is publicly accessible.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request, id):
        artist = Artist.objects.get(id=id)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)


class ReleaseGroupAPI(APIView):
    """
    View to get information about a release group.

    This view is publicly accessible.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request, id):
        release_group = ReleaseGroup.objects.get(id=id)
        serializer = ReleaseGroupSerializer(release_group)
        return Response(serializer.data)


class RecordingAPI(APIView):
    """
    View to get information about a recording.

    This view is publicly accessible.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request, id):
        recording = Recording.objects.get(id=id)
        serializer = RecordingSerializer(recording)
        return Response(serializer.data)


class TrackAPI(APIView):
    """
    View to get information about a track.

    This view is publicly accessible.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request, id):
        track = Track.objects.get(id=id)
        serializer = TrackSerializer(track)
        return Response(serializer.data)


class RecordingAPI2(APIView):
    """
    View to get information about a recording.

    This view is publicly accessible.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request, id):
        recording = Recording.objects.get(id=id)
        serializer = RecordingSerializer2(recording)
        return Response(serializer.data)