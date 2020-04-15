from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import ExceptionLog


class ExceptionLogList(View, LoginRequiredMixin):
    """
    View to list exceptions that have been logged with their
    tracebacks.
    """

    def get(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied
        else:
            logs = ExceptionLog.objects.all().order_by("-occured_on")
            paginator = Paginator(
                logs, 100, orphans=50, allow_empty_first_page=True
            )
            page_no = request.GET.get("page", default=1)

            try:
                page = paginator.page(page_no)
            except EmptyPage:  # We check that the requested page exists.
                # If not, the last page is displayed.
                page = paginator.page(paginator.num_pages)

            # Remember that the entries are displayed in reverse chronological order.
            # This variables are needed to display the beginning and end dates of the
            # current page.
            if logs.count() > 0:
                last_log = page.object_list[0]
                num_log_this_page = len(page.object_list)
                first_log = page.object_list[num_log_this_page - 1]

            return render(request, "tools/exception_log_list.html", locals())


class ExceptionLogDisplay(View, LoginRequiredMixin):
    """
    View to display an exception that has been logged with its
    traceback.
    """

    def get(self, request, id):
        if not request.user.is_superuser:
            raise PermissionDenied
        else:
            log = get_object_or_404(ExceptionLog, id=id)
            traceback_list = []
            for i, line in enumerate(log.traceback.split("\n")):
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
