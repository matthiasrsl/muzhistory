from django.urls import path

from . import views

app_name="tools"
urlpatterns = [
    path("exception_log/<int:id>", views.ExceptionLogDisplay.as_view(), name="log_display"),
]
