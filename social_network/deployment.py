import os
from .settings import *
from .settings import BASE_DIR


SECRET_KEY = os.environ['SECRET']
ALLOWED_HOST = [os.environ['WEBSITE_HOSTNAME']]

CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
DEBUG = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STORAGES = {
    "default" : {
        "BACKEND" : "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles" : {
        "BACKEND" : "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')

connection_string = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
parameters = {}
for pair in connection_string.split(' '):
    if '=' in pair:
        key, value = pair.split('=')
        parameters[key] = value
    else:
        # Handle malformed pairs here if necessary
        pass

DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parameters['dbname'],
        'HOST': parameters['host'],
        'USER': parameters['user'],
        'PASSWORD': parameters['password'],
    }
}
