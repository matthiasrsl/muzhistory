"""muzhistory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from history.views import HistoryOverview
from frontend.views import app

urlpatterns = [
    path("", HistoryOverview.as_view(), name="overview"),
    path("admin_fgcrel/", admin.site.urls),
    path("tools_nqztht/", include("tools.urls", namespace="tools")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("history/", include("history.urls", namespace="history")),
    path("api/", include("api.urls", namespace="api")),
    re_path('^(.*)$', app, name="app"),
]
