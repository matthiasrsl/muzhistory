from django.db import models

from musicdata.models import *

class DeezerAlbum(Release):
    """
    Represents an album in Deezer's database.
    """
    dz_id = models.BigIntegerField(null=True, blank=True)
