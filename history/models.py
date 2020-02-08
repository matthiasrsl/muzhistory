from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.conf import settings


class HistoryEntry(models.Model):
    version = models.IntegerField(default=settings.MH_VERSION)
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    track_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    track = GenericForeignKey('track_type', 'object_id')
    timestamp = models.PositiveIntegerField(null=True, blank=True)
    listening_datetime = models.DateTimeField() 
            # Consistent with timestamp if it is not null.
