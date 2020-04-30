"""
Django settings for ayudapy project.
Generated by 'django-admin startproject' using Django 2.2.11.
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ
import logging
import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'leaflet',
    'django.contrib.gis',
    'core',
    'widget_tweaks',
    'rest_framework',
    'rest_framework_gis',
    'django_filters',
    'simple_history',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'conf.context_processors.global_vars'
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    'default': env.db('DATABASE_URL')
}
if not DEBUG:
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'allstatic')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATIC_URL = '/static/'

MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'

LATITUDE_MAPS = str(env('LATITUDE_MAPS'))
LONGITUDE_MAPS = str(env('LONGITUDE_MAPS'))
DEFAULT_ZOOM_MAPS = env('DEFAULT_ZOOM', default=13)
MIN_ZOOM_MAPS = env('MIN_ZOOM_MAPS', default=3)
MAX_ZOOM_MAPS = env('MAX_ZOOM_MAPS', default=18)
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (LATITUDE_MAPS, LONGITUDE_MAPS),
    'DEFAULT_ZOOM': DEFAULT_ZOOM_MAPS,
    'MIN_ZOOM': MIN_ZOOM_MAPS,
    'MAX_ZOOM': MAX_ZOOM_MAPS,
    'RESET_VIEW': False,
    'NO_GLOBALS': False,

    'PLUGINS': {
        'markercluster': {
            'css': 'https://leaflet.github.io/Leaflet.markercluster/dist/MarkerCluster.Default.css',
            'js': 'https://leaflet.github.io/Leaflet.markercluster/dist/leaflet.markercluster-src.js',
            'auto-include': True,
        },
        'fullscreen': {
            'css': 'https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/leaflet.fullscreen.css',
            'js': 'https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/Leaflet.fullscreen.min.js',
            'auto-include': True,
        },
    }
}


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        #'rest_framework.renderers.BrowsableAPIRenderer',  # Uncomment this like if you want to use the nice API view for dev
    )
}

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'

URL_PRINCIPAL = env('URL_PRINCIPAL', default='https://argentinaporvos.org')
USE_S3 = False if DEBUG else True
# STORAGES
if USE_S3:
    # https://django-storages.readthedocs.io/en/latest/#installation
    INSTALLED_APPS += ["storages"]  # noqa F405
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_QUERYSTRING_AUTH = False
    # DO NOT change these unless you know what you're doing.
    _AWS_EXPIRY = 60 * 60 * 24 * 7
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate"
    }
    #  https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_DEFAULT_ACL = None
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_S3_REGION_NAME = env("DJANGO_AWS_S3_REGION_NAME", default=None)
    # STATIC
    # ------------------------
    STATICFILES_STORAGE = "conf.settings.StaticRootS3Boto3Storage"
    # MEDIA
    # ------------------------------------------------------------------------------
    # region http://stackoverflow.com/questions/10390244/
    # Full-fledge class: https://stackoverflow.com/a/18046120/104731
    from storages.backends.s3boto3 import S3Boto3Storage  # noqa E402


    class StaticRootS3Boto3Storage(S3Boto3Storage):
        location = "static"
        default_acl = "public-read"


    class MediaRootS3Boto3Storage(S3Boto3Storage):
        location = "media"
        file_overwrite = False


    # endregion
    DEFAULT_FILE_STORAGE = "conf.settings.MediaRootS3Boto3Storage"
    MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/"


GOOGLE_TAG_MANAGER_ID = env('GOOGLE_TAG_MANAGER_ID', default=None)

if not DEBUG:
    # Sentry
    SENTRY_DSN = env("SENTRY_DSN")
    SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

    sentry_logging = LoggingIntegration(
        level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors as events
    )
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[sentry_logging, DjangoIntegration()],
    )
