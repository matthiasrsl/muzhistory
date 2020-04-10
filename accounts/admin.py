from django.contrib import admin

from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "track_location", "version")
    list_filter = ("track_location", "version")
    search_fields = ("user",)


admin.site.register(Profile, ProfileAdmin)
