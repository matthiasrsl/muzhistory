from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.display_profile),
    path('link_deezer/', views.GetDeezerOAuthCode.as_view()),
]
