import datetime as dt

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Sum, Count
from django.db.models.query import EmptyQuerySet
from django.shortcuts import redirect, render
from django.utils import timezone as tz
from django.views import View

from accounts.models import Profile
from history.models import HistoryEntry
from musicdata.models import Track, Artist


class HistoryOverview(View, LoginRequiredMixin):
    """
    Displays the listening history of the logged user.
    """

    def get(self, request):
        profile = request.user.profile
        last_history_request = (
            profile.platformaccount_set.all()
            .order_by("-last_history_request")[0]
            .last_history_request
        )

        entries = (
            HistoryEntry.objects.select_related(
                "track",
                "track__deezertrack__release",
                "track__deezertrack__release__release_group",
                "track__recording",
            )
            .filter(profile=profile)
            .order_by("-listening_datetime")
        )
        paginator = Paginator(
            entries, 150, orphans=50, allow_empty_first_page=True
        )
        total_listening_duration = entries.aggregate(
            Sum("track__deezertrack__duration")
        )
        if not total_listening_duration["track__deezertrack__duration__sum"]:
            total_listening_duration_seconds = 0
        else:
            total_listening_duration_seconds = total_listening_duration[
                "track__deezertrack__duration__sum"
            ]
            date_first_entry = entries.earliest(
                "listening_datetime"
            ).listening_datetime
        total_listening_duration_hours = total_listening_duration_seconds // 60
        total_listening_timedelta = dt.timedelta(
            seconds=total_listening_duration_seconds
        )

        page_number = request.GET.get("page", default=1)
        try:
            page = paginator.page(page_number)
        except EmptyPage:  # We check that the requested page exists.
            # If not, the last page is displayed.
            page = paginator.page(paginator.num_pages)

        # Remember that the entries are displayed in reverse chronological
        # order.
        # This variables are needed to display the beginning and end dates of
        # the current page.
        if paginator.count > 0:
            last_entry = page.object_list[0]
            entry_count_current_page = len(page.object_list)
            first_entry = page.object_list[entry_count_current_page - 1]

        response = render(request, "history/history_overview.html", locals())
        return response


class Statistics(View, LoginRequiredMixin):
    """
    Statistics regarding the complete history.
    """

    def get(self, request):
        DEFAULT_ALBUM_COVER_URL = settings.DEFAULT_ALBUM_COVER_URL
        profile = request.user.profile
        entries = HistoryEntry.objects.filter(profile=profile)
        if not entries:
            empty_history = True
            return render(request, "history/statistics.html", locals())
        else:
            empty_history = False
        now = tz.now()
        entries_last_7days = entries.filter(
            listening_datetime__gte=now.date() - dt.timedelta(days=7)
        )
        entries_this_month = entries.filter(
            listening_datetime__gte=now.date() - dt.timedelta(days=30)
        )
        entries_this_year = entries.filter(listening_datetime__year=now.year)

        # All time
        artists_all_time = (
            Artist.objects.filter(
                recording__track__historyentry__profile=profile,
                recording__track__historyentry__entry_type="listening",
            )
            .annotate(entry_count=Count("recording__track__historyentry"))
            .order_by("-entry_count")[:5]
        )

        tracks_all_time = (
            Track.objects.filter(
                historyentry__profile=profile,
                historyentry__entry_type="listening",
            )
            .annotate(entry_count=Count("historyentry"))
            .order_by("-entry_count")[:10]
        )

        # This year
        artists_this_year = (
            Artist.objects.filter(
                recording__track__historyentry__profile=profile,
                recording__track__historyentry__entry_type="listening",
                recording__track__historyentry__listening_datetime__year=tz.now().year,
            )
            .annotate(entry_count=Count("recording__track__historyentry"))
            .order_by("-entry_count")[:5]
        )

        tracks_this_year = (
            Track.objects.filter(
                historyentry__profile=profile,
                historyentry__entry_type="listening",
                historyentry__listening_datetime__year=tz.now().year,
            )
            .annotate(entry_count=Count("historyentry"))
            .order_by("-entry_count")[:10]
        )

        # Last 30 days
        artists_30_days = (
            Artist.objects.filter(
                recording__track__historyentry__profile=profile,
                recording__track__historyentry__entry_type="listening",
                recording__track__historyentry__listening_datetime__gte=(
                    now.date() - dt.timedelta(days=30)
                ),
            )
            .annotate(entry_count=Count("recording__track__historyentry"))
            .order_by("-entry_count")[:5]
        )

        tracks_30_days = (
            Track.objects.filter(
                historyentry__profile=profile,
                historyentry__entry_type="listening",
                historyentry__listening_datetime__gte=(
                    now.date() - dt.timedelta(days=30)
                ),
            )
            .annotate(entry_count=Count("historyentry"))
            .order_by("-entry_count")[:10]
        )

        # Last 7 days
        artists_last_7days = (
            Artist.objects.filter(
                recording__track__historyentry__profile=profile,
                recording__track__historyentry__entry_type="listening",
                recording__track__historyentry__listening_datetime__gte=(
                    now.date() - dt.timedelta(days=7)
                ),
            )
            .annotate(entry_count=Count("recording__track__historyentry"))
            .order_by("-entry_count")[:5]
        )

        tracks_last_7days = (
            Track.objects.filter(
                historyentry__profile=profile,
                historyentry__entry_type="listening",
                historyentry__listening_datetime__gte=(
                    now.date() - dt.timedelta(days=7)
                ),
            )
            .annotate(entry_count=Count("historyentry"))
            .order_by("-entry_count")[:10]
        )

        stats_sections = [
            {
                "title": "Les 7 derniers jours",
                "objects": {
                    "artists": artists_last_7days,
                    "tracks": tracks_last_7days,
                },
            },
            {
                "title": "Les 30 derniers jours",
                "objects": {
                    "artists": artists_30_days,
                    "tracks": tracks_30_days,
                },
            },
            {
                "title": tz.now().year,
                "objects": {
                    "artists": artists_this_year,
                    "tracks": tracks_this_year,
                },
            },
            {
                "title": "Tout l'historique",
                "objects": {
                    "artists": artists_all_time,
                    "tracks": tracks_all_time,
                },
            },
        ]

        return render(request, "history/statistics.html", locals())
