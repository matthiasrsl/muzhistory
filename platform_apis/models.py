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
