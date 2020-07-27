from django.contrib.auth.models import User

from rest_framework import serializers

from accounts.models import Profile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(source='pk', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'date_joined')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ('id', 'version', 'user', 'track_location')