from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

app_name= "accounts"
urlpatterns = [
    path("profile/", views.DisplayProfile.as_view(), name="display-profile"),
    path("link_deezer/", views.GetDeezerOAuthCode.as_view()),
    path("login/", LoginView.as_view(template_name="accounts/login.html"))
]
