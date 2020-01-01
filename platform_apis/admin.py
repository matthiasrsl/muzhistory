from django.contrib import admin
from .models import *

class MarketAdmin(admin.ModelAdmin):
    list_display = ('english_name', 'code', 'version')
    list_filter = ('version',)
    search_fields = ('english_name', 'code')
    

admin.site.register(Market, MarketAdmin)
