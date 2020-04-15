import traceback
import sys

from django.db import models
from django.utils import timezone as tz


class ExceptionLog(models.Model):
    exception_name = models.CharField(max_length=100)
    exception_module = models.CharField(max_length=1000)
    exception_value = models.CharField(max_length=1000)
    function_name = models.CharField(max_length=1000)
    traceback = models.TextField()
    occured_on = models.DateTimeField()


def log_exceptions(fn_ififoqu):
    """
    Executes the decorated function and if an exception occurs,
    stores it in the database with its traceback.
    """
    # The weird names are to unequivocally detect frames related to 
    # this decorator in the traceback.
    def wrapped_izfgzi(*args, **kwargs):
        try:
            return fn_ififoqu(*args, **kwargs)
        except Exception as e:
            now = tz.now()
            e_type, e_val, e_traceback = sys.exc_info()
            traceback_text = "".join(
                traceback.format_exception(e_type, e_val, e_traceback)
            )
            entry = ExceptionLog.objects.create(
                exception_name=e_type.__name__,
                exception_module=e_type.__module__,
                exception_value=str(e_val),
                function_name=str(fn_ififoqu).split(' ')[1],
                traceback=traceback_text,
                occured_on=now
            )
            entry.save()
            raise

    return wrapped_izfgzi
