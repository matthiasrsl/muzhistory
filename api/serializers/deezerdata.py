from rest_framework import serializers
from deezerdata.models.deezer_objects import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('version', 'user', 'track_location')