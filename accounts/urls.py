from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.DisplayProfile.as_view(), name="display-profile"),
    path("link_deezer/", views.GetDeezerOAuthCode.as_view()),
]
