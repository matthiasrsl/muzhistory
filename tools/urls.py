from django.urls import path

from . import views

urlpatterns = [
    path("exception_log/<int:id>", views.ExceptionLogDisplay.as_view()),
]
