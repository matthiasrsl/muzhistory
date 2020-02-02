from django.db import models

from django.conf import settings

class DeezerApiError(Exception):
    """
    To be raised when a query to the deezer api returns an error.
    """
    def __init__(self, error_type, message, code):
        self.error_type = error_type
        self.message = message
        self.code = code
        
    def __str__(self):
        return "{} ({}): {}".format(self.error_type, self.code, self.message)
        

class DeezerOAuthError(Exception):
    """
    To be raised when OAuth authentication fails.
    """
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message
        

class DeezerRefusedAccessError(Exception):
    """
    To be raised when the user doesn't allow access to their Deezer
    account during the OAuth process.
    """
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message


class Market(models.Model):
    version = models.IntegerField(default=settings.MH_VERSION)
    code = models.CharField(max_length=2)  # ISO 3166-1 alpha-2.
    english_name = models.CharField(max_length=100, null=True);
