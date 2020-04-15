from django.urls import path

from . import views

app_name="tools"
urlpatterns = [
    path("exceptionlog/<int:id>", views.ExceptionLogDisplay.as_view(), name="log_display"),
    path("exceptionlogslist", views.ExceptionLogList.as_view(), name="log_list"),
]
