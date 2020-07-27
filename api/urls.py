from django.urls import path

from .views.accounts import ProfileAPI
from .views.musicdata import *

app_name= "api"
urlpatterns = [
    path("profile", ProfileAPI.as_view()),
    path("artist/<int:id>", ArtistAPI.as_view()),
    path("releasegroup/<int:id>", ReleaseGroupAPI.as_view()),
    path("recording/<int:id>", RecordingAPI.as_view()),
    path("track/<int:id>", TrackAPI.as_view()),
]
