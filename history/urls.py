from django.urls import path

from . import views


app_name = "history"
urlpatterns = [
    path("overview/", views.HistoryOverview.as_view(), name="overview"),
    path("stats/", views.Statistics.as_view(), name="statistics"),
]
