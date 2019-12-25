from django.contrib import admin

from .models import *

class DeezerAlbumAdmin(admin.ModelAdmin):
    list_display = ('release_group', 'dz_id', 'available', 'version')
    list_display_links = ('release_group', )
    list_filter = ('version', 'available')
    search_fields = ('release_group__title',)
    
class DeezerTrackAdmin(admin.ModelAdmin):
    list_display = ('recording', 'dz_id', 'readable', 'version')
    list_display_links = ('recording',)
    list_filter = ('readable', 'version',)
    search_fields = ('recording__title', 'dz_id')
    
class DeezerMp3Admin(admin.ModelAdmin):
    list_display = ('title', 'artist_name', 'album_name', 'version')
    list_filter = ('version',)
    search_fields = ('title', 'dz_id')
    
admin.site.register(DeezerAlbum, DeezerAlbumAdmin)
admin.site.register(DeezerTrack, DeezerTrackAdmin)
admin.site.register(DeezerMp3, DeezerMp3Admin)