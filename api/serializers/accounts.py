from django.contrib.auth.models import User
from django.db.models import Sum, Min

from rest_framework import serializers

from accounts.models import Profile
from history.models import HistoryEntry


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "date_joined")


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    nb_listenings = serializers.SerializerMethodField("get_nb_listenings")
    listening_duration = serializers.SerializerMethodField(
        "get_listening_duration"
    )
    last_update = serializers.SerializerMethodField("get_last_update")

    def get_nb_listenings(self, obj):
        entries = HistoryEntry.objects.filter(profile=obj)
        return entries.count()

    def get_listening_duration(self, obj):
        entries = HistoryEntry.objects.filter(profile=obj)
        return entries.aggregate(result=Sum("track__deezertrack__duration"))[
            "result"
        ]

    def get_last_update(self, obj):
        return obj.platformaccount_set.aggregate(
            result=Min("last_history_request")
        )["result"]

    class Meta:
        model = Profile
        fields = (
            "id",
            "version",
            "user",
            "track_location",
            "nb_listenings",
            "listening_duration",
            "last_update",
        )
