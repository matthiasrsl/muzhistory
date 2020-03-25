# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-

import os

import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()
env.read_env(env.str('ENV_PATH', os.path.join(BASE_DIR, '.env')))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# False if not in os.environ
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['deezhistory.pythonanywhere.com', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'tools',
    'platform_apis',
    'musicdata',
    'deezerdata',
    # Debugging, testing and documentation tools.
    # 'django_nose',
    'django_extensions',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Testing

'''
# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package= tools.models, tools.admin, \
            platform_apis.models, platform_apis.admin, \
            musicdata.models, musicdata.admin, \
            deezerdata.models, deezerdata.admin',
]
'''
# Custom settings

LOG_RETRIEVAL = True
