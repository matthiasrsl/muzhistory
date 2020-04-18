from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.DisplayProfile.as_view()),
    path("link_deezer/", views.GetDeezerOAuthCode.as_view()),
]
