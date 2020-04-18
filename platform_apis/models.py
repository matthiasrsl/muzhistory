from django.conf import settings
from django.db import models


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
    english_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.code



class PlatformAccount(models.Model):
    """
    A user account on a music streaming platform.
    """
    class StatusChoices(models.TextChoices):
        ACTIVE = "act", "Active"
        INACTIVE = "ina", "Inactive"
        BLOCKED = "blo", "Blocked"

    version = models.IntegerField(default=settings.MH_VERSION)
    status = models.CharField(
        max_length=3,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )
    profile = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, null=True
    )
    user_id = models.CharField(max_length=100)
    access_token = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(blank=True)
    market = models.ForeignKey(
        "platform_apis.Market", on_delete=models.PROTECT, null=True, blank=True
    )
    last_history_request = models.DateTimeField(
        null=True, blank=True, default=settings.OLDEST_DATE
    )
    name = models.CharField(max_length=300)
    # link = models.URLField(max_length=2000)
