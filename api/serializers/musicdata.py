from django.conf import settings

from rest_framework import serializers

from musicdata.models import (
    Artist,
    ReleaseGroup,
    Release,
    Recording,
    RecordingContribution,
    Track,
)
from deezerdata.models.deezer_objects import DeezerMp3


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        fields = ("id", "name", "image_url_deezer_medium")


class ReleaseGroupSerializer(serializers.ModelSerializer):
    contributors = ArtistSerializer(many=True)

    class Meta:
        model = ReleaseGroup
        fields = ("id", "title", "album_type", "contributors")


class RecordingContributionSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.ReadOnlyField(source="artist.name")
    role = serializers.ReadOnlyField()

    class Meta:
        model = RecordingContribution
        fields = ("name", "role")


class RecordingSerializer(serializers.Serializer):
    title = serializers.SerializerMethodField("get_title")
    title_refine = serializers.SerializerMethodField("get_title_refine")
    contributors = serializers.SerializerMethodField("get_contributors")
    album_cover = serializers.SerializerMethodField("get_album_cover")
    preview = serializers.SerializerMethodField("get_preview")

    def get_title(self, obj):
        if obj.deezer_track:
            return obj.deezer_track.title_short
        else:
            return obj.title

    def get_title_refine(self, obj):
        if obj.deezer_track:
            return obj.deezer_track.title_version
        else:
            return ""

    def get_contributors(self, obj):
        if obj.deezer_track:
            try:
                mp3 = obj.deezer_track.deezermp3
                return [{"name": mp3.artist_name, "role": "undef"}]
            except DeezerMp3.DoesNotExist:
                return [
                    RecordingContributionSerializer(contrib).data
                    for contrib in obj.recordingcontribution_set.all()
                ]

    def get_album_cover(self, obj):
        if obj.deezer_track:
            try:
                mp3 = obj.deezer_track.deezermp3
                return settings.DEFAULT_ALBUM_COVER_URL
            except DeezerMp3.DoesNotExist:
                return obj.deezer_track.release.cover_medium
        else:
            return settings.DEFAULT_ALBUM_COVER_URL

    def get_preview(self, obj):
        if obj.deezer_track:
            return obj.deezer_track.preview
        else:
            return ""

class TrackSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    track_type = serializers.CharField(max_length=20)
    disc_number = serializers.IntegerField()
    track_number = serializers.IntegerField()

    duration = serializers.SerializerMethodField("get_duration")
    album_title = serializers.SerializerMethodField("get_album_title")
    album_cover = serializers.SerializerMethodField("get_album_cover")
    title = serializers.SerializerMethodField("get_title")
    title_refine = serializers.SerializerMethodField("get_title_refine")

    contributors = serializers.SerializerMethodField("get_contributors")
    preview = serializers.SerializerMethodField("get_preview")


    def get_duration(self, obj):
        if obj.deezertrack:
            return obj.deezertrack.duration
        else:
            return 0

    def get_album_title(self, obj):
        if obj.deezertrack:
            try:
                return obj.deezertrack.deezermp3.album_name
            except DeezerMp3.DoesNotExist:
                return obj.deezertrack.release.release_group.title
        else:
            return ""

    def get_title(self, obj):
        if obj.deezertrack:
            return obj.deezertrack.title_short
        else:
            return obj.title

    def get_title_refine(self, obj):
        if obj.deezertrack:
            return obj.deezertrack.title_version
        else:
            return ""

    def get_contributors(self, obj):
        if obj.deezertrack:
            try:
                mp3 = obj.deezertrack.deezermp3
                return [{"name": mp3.artist_name, "role": "undef"}]
            except DeezerMp3.DoesNotExist:
                return [
                    RecordingContributionSerializer(contrib).data
                    for contrib in obj.recording.recordingcontribution_set.all()
                ]

    def get_album_cover(self, obj):
        if obj.deezertrack:
            try:
                mp3 = obj.deezertrack.deezermp3
                return settings.DEFAULT_ALBUM_COVER_URL
            except DeezerMp3.DoesNotExist:
                return obj.deezertrack.release.cover_medium
        else:
            return settings.DEFAULT_ALBUM_COVER_URL

    def get_preview(self, obj):
        if obj.deezertrack:
            return obj.deezertrack.preview
        else:
            return ""
