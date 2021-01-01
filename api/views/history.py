from django.conf import settings
from django.shortcuts import redirect, render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


from history.models import HistoryEntry
from accounts.models import Profile
from api.serializers.history import HistoryEntrySerializer
from api.serializers.accounts import ProfileSerializer


class HistoryAPI(APIView):
    """
    View to get a profile history entries.

    This view only accessible to logged users.
    """

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = []

    def get(self, request):
        if request.user.is_authenticated:
            profile = request.user.profile
        else:
            profile = Profile.objects.filter(showcase_profile=True)[0]
        entries = HistoryEntry.objects.filter(profile=profile).order_by(
            "-listening_datetime"
        )[:100]

        serializer_entries = HistoryEntrySerializer(entries, many=True)
        serializer_profile = ProfileSerializer(profile)
        response = {
            "data": serializer_entries.data,
            "profile": serializer_profile.data,
        }

        return Response(response)
