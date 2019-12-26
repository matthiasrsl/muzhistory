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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Custom settings

LOG_RETRIEVAL = True
