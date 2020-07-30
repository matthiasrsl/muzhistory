from django.conf import settings
from django.shortcuts import redirect, render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


from history.models import HistoryEntry
from api.serializers.history import HistoryEntrySerializer


class HistoryAPI(APIView):
    """
    View to get a profile history entries.

    This view only accessible to logged users.
    """

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        entries = HistoryEntry.objects.filter(profile=profile).order_by(
            "-listening_datetime"
        )

        serializer = HistoryEntrySerializer(entries, many=True)
        response = {"data": serializer.data}

        return Response(response)
