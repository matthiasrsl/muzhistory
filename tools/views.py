from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import View

from .models import ExceptionLog


class ExceptionLogDisplay(View, LoginRequiredMixin):
    """
    View to display an exception that has been logged with its
    traceback.
    """

    def get(self, request, id):
        if request.user.is_superuser:
            log = get_object_or_404(ExceptionLog, id=id)
            traceback_list = []
            for i,line in enumerate(log.traceback.split("\n")):
                if "wrapped_izfgzi" in line or "fn_ififoqu" in line:
                    line_type = "logging"
                elif line[:9] == "Traceback":
                    line_type = "begin_tb"
                elif line[:6] == "  File":
                    line_type = "file"
                    if not "muzhistory" in line:
                        line_type = "file_dependency"
                elif line[:15] == "During handling":
                    line_type = "embedded"
                elif line[:9] == "The above":
                    line_type = "chaining"
                elif line[:4] == "    ":
                    line_type = "line"
                elif line == "":
                    line_type = "empty"
                else:
                    line_type = "exception"
                
                if i > 0:
                    if traceback_list[-1][0] == "file_dependency":
                        line_type = "line_dependency"

                """ line_list = []
                while len(line) > 140:
                    line_list.append(line[:140])
                    line = line[140:]
                line_list.append(line)
                line = '\n'.join(line_list) """
                traceback_list.append((line_type, line))

            return render(
                request, "tools/exception_log_display.html", locals()
            )

        else:
            raise PermissionDenied
