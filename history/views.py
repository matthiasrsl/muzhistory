import datetime as dt

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Sum, Count
from django.db.models.query import EmptyQuerySet
from django.shortcuts import redirect, render
from django.views import View

from accounts.models import Profile
from history.models import HistoryEntry


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
