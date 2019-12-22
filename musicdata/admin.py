from django.contrib import admin

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'deezer_id', 'spotify_id', 'version')
    list_filter = ('version',)
    search_fields = ('name', 'dz_id')
