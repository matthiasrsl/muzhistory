from django.contrib import admin

from .models import *


class HistoryEntryAdmin(admin.ModelAdmin):
    list_display = ("profile", "track", "listening_datetime")
    list_filter = ("profile",)
    search_fields = ("track", "profile")
    date_hierarchy = "listening_datetime"


admin.site.register(HistoryEntry, HistoryEntryAdmin)
