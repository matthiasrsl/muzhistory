from django.urls import path

from . import views

app_name= "accounts"
urlpatterns = [
    path("profile/", views.DisplayProfile.as_view(), name="display-profile"),
    path("link_deezer/", views.GetDeezerOAuthCode.as_view()),
    path("api/profile", views.ProfileAPI.as_view()),
]
