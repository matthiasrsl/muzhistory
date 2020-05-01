"""
Django settings for muzhistory project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import datetime as dt
import os

from django.utils import timezone as tz

import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()
env.read_env(env.str("ENV_PATH", os.path.join(BASE_DIR, ".env")))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["muzhistory.eu.pythonanywhere.com"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "admin_reorder",
    "muzhistory.apps.MyAdminConfig",
    "tools",
    "platform_apis",
    "accounts",
    "history",
    "musicdata",
    "deezerdata",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
]

ROOT_URLCONF = "muzhistory.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates"),],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "muzhistory.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "muzhistory$default",
        "USER": "muzhistory",
        "PASSWORD": env("MYSQL_PASSWORD"),
        "HOST": "muzhistory.mysql.eu.pythonanywhere-services.com",
        "OPTIONS": {
            "read_default_file": "/path/to/my.cnf",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Security

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_REFERRER_POLICY = "same-origin"

SECURE_HSTS_SECONDS = 3600

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

# Authentication

LOGIN_URL = "/accounts/login/"

LOGIN_REDIRECT_URL = "history:overview"

LOGOUT_REDIRECT_URL = "/accounts/login/"

# Email sending

EMAIL_HOST = "smtp.gmail.com"

EMAIL_HOST_USER = "contact.muzhistory@gmail.com"

EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_USE_SSL = False

ADMINS = (
    ("Matthias Roussel", "mbluesblack01@gmail.com"),
)

# Misc

APPEND_SLASH = True

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

SESSION_COOKIE_AGE = 365 * 24 * 3600

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

ADMIN_REORDER = (
    "auth",
    "accounts",
    "history",
    "platform_apis",
    "musicdata",
    "deezerdata",
    "tools",
)

#  Custom settings

OLDEST_DATE = tz.make_aware(dt.datetime(year=1970, month=1, day=1))

MH_VERSION = 33

LOG_RETRIEVAL = False

ALWAYS_UPDATE_DEEZER_DATA = False

OPENWEATHER_API_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

OPENWEATHER_API_FORECAST_URL = (
    "https://api.openweathermap.org/data/2.5/forecast"
)

DEEZER_API_APP_ID = 409782

DEEZER_API_SECRET_KEY = env("DEEZER_API_SECRET_KEY")

DEEZER_AUTH_REDIRECT_URI = (
    "https://muzhistory.eu.pythonanywhere.com/accounts/link_deezer/"
)

DEEZER_ACCESS_TOKEN_URL = "https://connect.deezer.com/oauth/access_token.php"

DEEZER_OAUTH_URL = "https://connect.deezer.com/oauth/auth.php?app_id={}&redirect_uri={}&perms=basic_access,email,offline_access,listening_history"

DEEZER_API_USER_URL = "https://api.deezer.com/user/me"

DEEZER_API_HISTORY_URL = "https://api.deezer.com/user/{}/history"

DEEZER_API_TRACK_URL = "https://api.deezer.com/track/{}"

DEEZER_API_TRACK_BY_ISRC_URL = "https://api.deezer.com/2.0/track/isrc:{}"

DEEZER_API_ALBUM_URL = "https://api.deezer.com/album/{}"

DEEZER_API_ARTIST_URL = "https://api.deezer.com/artist/{}"

DEFAULT_ALBUM_COVER_URL = "https://e-cdns-images.dzcdn.net/images/cover/d41d8cd98f00b204e9800998ecf8427e/380x380-000000-80-0-0.jpg"


try:
    from .local_settings import *  # Developpement settings.
except ImportError as e:
    pass
