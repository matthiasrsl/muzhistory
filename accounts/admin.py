from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'track_location', 'version')
    list_filter = ('track_location', 'version')
    search_fields = ('user', )
    
class DeezerAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile', 'user_id', 'last_history_request',
            'version')
    list_filter = ('version', )
    date_hierarchy = 'inscription_date'
    search_fields = ('name', 'firstname', 'lastname')
    
    
admin.site.register(Profile, ProfileAdmin)
admin.site.register(DeezerAccount, DeezerAccountAdmin)
