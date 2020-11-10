from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render

from requests.exceptions import RequestException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


from platform_apis.models import DeezerOAuthError
from deezerdata.models.deezer_account import DeezerAccount

from accounts.models import Profile
from api.serializers.accounts import ProfileSerializer



class ProfileAPI(APIView):
    """
    View to get information about the logged user.

    Only authenticated users can access this view.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)