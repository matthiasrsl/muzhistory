from django.contrib import admin

from .models import *

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'deezer_id', 'spotify_id', 'version')
    list_filter = ('version',)
    search_fields = ('name', 'dz_id')
    
class ReleaseGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'album_type', 'version')
    list_filter = ('album_type', 'version',)
    search_fields = ('title',)
    
class RecordingAdmin(admin.ModelAdmin):
    list_display = ('title', 'isrc', 'version')
    list_filter = ('version',)
    search_fields = ('name', 'isrc')
    
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'dz_id', 'version')
    list_filter = ('version',)
    search_fields = ('name', 'dz_id')
    
class ReleaseGroupContributionAdmin(admin.ModelAdmin):
    list_display = ('artist', 'release_group', 'role', 'version')
    list_display_links = ('release_group', )
    list_filter = ('role', 'version')
    search_fields = ('artist', 'release_group__title')
    
class RecordingContributionAdmin(admin.ModelAdmin):
    list_display = ('artist', 'recording', 'role', 'version')
    list_display_links = ('recording', )
    list_filter = ('role', 'version')
    search_fields = ('artist', 'recording__title')
    
admin.site.register(Artist, ArtistAdmin)
admin.site.register(ReleaseGroup, ReleaseGroupAdmin)
admin.site.register(Recording, RecordingAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(ReleaseGroupContribution, ReleaseGroupContributionAdmin)
admin.site.register(RecordingContribution, RecordingContributionAdmin)
