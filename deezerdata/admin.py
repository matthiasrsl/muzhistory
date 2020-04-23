from django.contrib import admin

from .models.deezer_account import *
from .models.deezer_objects import *


class DeezerAlbumAdmin(admin.ModelAdmin):
    list_display = ("name", "release_group", "dz_id", "available", "version")
    list_display_links = ("name",)
    list_filter = ("version", "available")
    search_fields = ("release_group__title",)

    def name(self, instance):
        return str(instance)


class DeezerTrackAdmin(admin.ModelAdmin):
    list_display = ("title_short", "recording", "dz_id", "readable", "version")
    list_display_links = ("title_short",)
    list_filter = (
        "readable",
        "version",
    )
    search_fields = ("recording__title", "dz_id")


class DeezerMp3Admin(admin.ModelAdmin):
    list_display = ("title_short", "artist_name", "album_name", "version")
    list_filter = ("version",)
    search_fields = ("title", "dz_id")


class DeezerAccountAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "profile",
        "user_id",
        "last_history_request",
        "version",
    )
    list_filter = ("version",)
    date_hierarchy = "inscription_date"
    search_fields = ("name", "firstname", "lastname")


admin.site.register(DeezerAlbum, DeezerAlbumAdmin)
admin.site.register(DeezerTrack, DeezerTrackAdmin)
admin.site.register(DeezerMp3, DeezerMp3Admin)
admin.site.register(DeezerAccount, DeezerAccountAdmin)
