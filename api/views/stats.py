from django.shortcuts import redirect, render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


from history.models import HistoryEntry
from accounts.models import Profile
from api.serializers.history import HistoryEntrySerializer
from api.serializers.accounts import ProfileSerializer
from api.serializers.musicdata import *

import datetime as dt

from django.conf import settings
from django.db.models import Count
from django.shortcuts import redirect, render
from django.utils import timezone as tz

from accounts.models import Profile
from history.models import HistoryEntry
from musicdata.models import Track, Artist, Recording
from deezerdata.models.deezer_objects import DeezerTrack


class StatsAPI(APIView):
    """
    View to get a profile listening statistics.

    This view only accessible to logged users.
    """

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = []

    def rank_elements(self, queryset):
        """
        Sorts elements and assign a rank to each, taking care of
        ex aequos.
        """
        rank, count, previous, result = 0, 0, None, {}
        for elt in queryset:
            count += 1
            if elt.entry_count != previous:
                rank += count
                previous = elt.entry_count
                count = 0
            elt.rank = rank

        return queryset

    def get(self, request):
        DEFAULT_ALBUM_COVER_URL = settings.DEFAULT_ALBUM_COVER_URL
        profile = request.user.profile
        entries = HistoryEntry.objects.filter(profile=profile)
        if not entries:
            empty_history = True
        else:
            empty_history = False
        now = tz.now()

        # All time
        artists_all_time = self.rank_elements(
            Artist.objects.filter(
                recording__track__historyentry__profile=profile,
                recording__track__historyentry__entry_type="listening",
            )
            .annotate(entry_count=Count("recording__track__historyentry"))
            .order_by("-entry_count", "name")[:9]
        )

        tracks_all_time = self.rank_elements(
            Recording.objects.filter(
                track__historyentry__profile=profile,
                track__historyentry__entry_type="listening",
            )
            .annotate(entry_count=Count("track__historyentry"))
            .order_by("-entry_count", "title")[:20]
        )

        # This year
        artists_this_year = self.rank_elements(
            Artist.objects.filter(
                recording__track__historyentry__profile=profile,
                recording__track__historyentry__entry_type="listening",
                recording__track__historyentry__listening_datetime__year=tz.now().year,
            )
            .annotate(entry_count=Count("recording__track__historyentry"))
            .order_by("-entry_count", "name")[:6]
        )

        tracks_this_year = self.rank_elements(
            Recording.objects.filter(
                track__historyentry__profile=profile,
                track__historyentry__entry_type="listening",
                track__historyentry__listening_datetime__year=tz.now().year,
            )
            .annotate(entry_count=Count("track__historyentry"))
            .order_by("-entry_count", "track")[:16]
        )

        # Last 30 days
        artists_30_days = self.rank_elements(
            Artist.objects.filter(
                recording__track__historyentry__profile=profile,
                recording__track__historyentry__entry_type="listening",
                recording__track__historyentry__listening_datetime__gte=(
                    now - dt.timedelta(days=30)
                ),
            )
            .annotate(entry_count=Count("recording__track__historyentry"))
            .order_by("-entry_count", "name")[:6]
        )

        tracks_30_days = self.rank_elements(
            Recording.objects.filter(
                track__historyentry__profile=profile,
                track__historyentry__entry_type="listening",
                track__historyentry__listening_datetime__gte=(
                    now - dt.timedelta(days=30)
                ),
            )
            .annotate(entry_count=Count("track__historyentry"))
            .order_by("-entry_count", "track")[:8]
        )

        # Last 7 days
        artists_last_7days = self.rank_elements(
            Artist.objects.filter(
                recording__track__historyentry__profile=profile,
                recording__track__historyentry__entry_type="listening",
                recording__track__historyentry__listening_datetime__gte=(
                    now - dt.timedelta(days=7)
                ),
            )
            .annotate(entry_count=Count("recording__track__historyentry"))
            .order_by("-entry_count", "name")[:3]
        )

        tracks_last_7days = self.rank_elements(
            Recording.objects.filter(
                track__historyentry__profile=profile,
                track__historyentry__entry_type="listening",
                track__historyentry__listening_datetime__gte=(
                    now - dt.timedelta(days=7)
                ),
            )
            .annotate(entry_count=Count("track__historyentry"))
            .order_by("-entry_count", "track")[:6]
        )

        response = {
            "empty_history": empty_history,

            "artists_all_time": ArtistSerializer(
                artists_all_time, many=True
            ).data,
            "tracks_all_time": RecordingSerializer(
                tracks_all_time, many=True
            ).data,

            "artists_this_year": ArtistSerializer(
                artists_this_year, many=True
            ).data,
            "tracks_this_year": RecordingSerializer(
                tracks_this_year, many=True
            ).data,

            "artists_30_days": ArtistSerializer(
                artists_30_days, many=True
            ).data,
            "tracks_30_days": RecordingSerializer(
                tracks_30_days, many=True
            ).data,

            "artists_7_days": ArtistSerializer(
                artists_last_7days, many=True
            ).data,
            "tracks_7_days": RecordingSerializer(
                tracks_last_7days, many=True
            ).data,
        }

        return Response(response)

