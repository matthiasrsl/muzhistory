from django.contrib.admin import ModelAdmin, register

from .models import *

@register(ExceptionLog)
class ExceptionLogAdmin(ModelAdmin):
    list_display = ('exception_name', 'occured_on')

