from django.urls import path

from . import views

app_name= "api"
urlpatterns = [
    path("profile", views.ProfileAPI.as_view()),
]
