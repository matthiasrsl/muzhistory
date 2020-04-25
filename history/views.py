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
from musicdata.models import Track, Artist, Recording


class HistoryOverview(LoginRequiredMixin, View):
    """
    Displays the listening history of the logged user.
    """
    def get(self, request):
        
        profile = Profile.objects.all()[0]
        last_history_request = (
            profile.platformaccount_set.all()
            .order_by("-last_history_request")[0]
            .last_history_request
        )

        DEFAULT_ALBUM_COVER_URL = settings.DEFAULT_ALBUM_COVER_URL
        entries = (
            HistoryEntry.objects.select_related(
                "track",
                "track__deezertrack__release",
                "track__deezertrack__release__release_group",
                "track__recording",
            )
            # .annotate(contrib='track__recording__recordingcontribution_set')
            .filter(profile=profile).order_by("-listening_datetime")
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
        total_listening_duration_hours = (
            total_listening_duration_seconds // 3600
        )
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


class Statistics(LoginRequiredMixin, View):
    """
    Statistics regarding the complete history.
    """
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
            return render(request, "history/statistics.html", locals())
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
            .order_by("-entry_count")[:9]
        )

        tracks_all_time = self.rank_elements(
            Recording.objects.filter(
                track__historyentry__profile=profile,
                track__historyentry__entry_type="listening",
            )
            .annotate(entry_count=Count("track__historyentry"))
            .order_by("-entry_count")[:20]
        )

        # This year
        artists_this_year = self.rank_elements(
            Artist.objects.filter(
                recording__track__historyentry__profile=profile,
                recording__track__historyentry__entry_type="listening",
                recording__track__historyentry__listening_datetime__year=tz.now().year,
            )
            .annotate(entry_count=Count("recording__track__historyentry"))
            .order_by("-entry_count")[:6]
        )

        tracks_this_year = self.rank_elements(
            Recording.objects.filter(
                track__historyentry__profile=profile,
                track__historyentry__entry_type="listening",
                track__historyentry__listening_datetime__year=tz.now().year,
            )
            .annotate(entry_count=Count("track__historyentry"))
            .order_by("-entry_count")[:16]
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
            .order_by("-entry_count")[:6]
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
            .order_by("-entry_count")[:8]
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
            .order_by("-entry_count")[:3]
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
            .order_by("-entry_count")[:6]
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
                "title": "Cette année",
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
