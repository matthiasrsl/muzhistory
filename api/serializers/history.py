from django.conf import settings

from rest_framework import serializers

from history.models import HistoryEntry
from .musicdata import TrackSerializer
from .accounts import ProfileSerializer

class HistoryEntrySerializer(serializers.ModelSerializer):
    track = TrackSerializer()

    class Meta:
        model = HistoryEntry
        fields = ("id", "entry_type", "track", "listening_datetime")