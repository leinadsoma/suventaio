from __future__ import absolute_import, unicode_literals

import os
import environ
from django.utils import six
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'l6jig7_*po@v152$-k2m@3pg5n5*&&c&w@v(yp+^e-k#r(#*vp'

DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'crispy_forms',
    'taggit',
    'mptt',
    'tagging',
    'project.app',
    #'djcelery',
    'corsheaders',
    'imagekit',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'project.app.context_processors.globalvar',
            ],
        },
    },
]

SITE_ID = 1

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'suventa.sqlite3',
        'USER': 'zaresdelweb',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

DATABASES['default']['ATOMIC_REQUESTS'] = True

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

LANGUAGE_CODE = 'es-MX'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    'static',
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

TAGGIT_CASE_INSENSITIVE = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
AUTH_USER_MODEL = 'app.User'
LOGIN_REDIRECT_URL = 'user_login'
LOGIN_URL = 'user_login'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
       {'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': ''},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4'}}

DEFAULT_FROM_EMAIL = ''
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = ''
EMAIL_USE_TLS = ''
EMAIL_SUBJECT_PREFIX = ''

APPTITLE = 'SuVenta'
APPTEXT = 'suventa'

PRODUCTION = False

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

BROKER_URL = 'redis://localhost/0'
CELERY_RESULT_BACKEND = "redis"
CELERYD_TASK_TIME_LIMIT = 600

CELERY_IMPORTS = ("project.app",)

#CELERYBEAT_SCHEDULE = {
    #'watchlist': { 
        #'task': 'project.app.tasks.WATCHLIST', 
        #'schedule': crontab(minute=0, hour=0),
        #'args': (), 
    #},
#}

CELERY_TIMEZONE = 'America/Mexico_City'

CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_IGNORE_RESULT = True

MPTT_ADMIN_LEVEL_INDENT = 20

try:
    from .var_production import *
    from boto.s3.connection import OrdinaryCallingFormat
    SECRET_KEY = VAR_SECRET_KEY

    AWS_ACCESS_KEY_ID = VAR_DJANGO_AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = VAR_AWS_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = VAR_AWS_STORAGE_BUCKET_NAME
    AWS_AUTO_CREATE_BUCKET = True
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()
    AWS_EXPIRY = 60 * 60 * 24 * 7
    AWS_HEADERS = {
        'Cache-Control': six.b('max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIRY, AWS_EXPIRY))
    }

    DEFAULT_FILE_STORAGE = 'config.s3utils.MediaRootS3BotoStorage'
    MEDIA_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
    STATICFILES_STORAGE = 'config.s3utils.StaticRootS3BotoStorage'
    STATIC_URL = 'https://s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME

    AWS_PRELOAD_METADATA = True

    FACEBOOK_APP_ID = VAR_FACEBOOK_APP_ID
    FACEBOOK_APP_SECRET = VAR_FACEBOOK_APP_SECRET

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'suventa',
            'USER': 'zaresdelweb',
            'PASSWORD': VAR_DATABASE_PASSWORD,
            'HOST': 'localhost',
            'PORT': '',
        }
    }

    DEFAULT_FROM_EMAIL = 'suventa <no_reply@suventa.com>'
    EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
    EMAIL_HOST_USER = VAR_EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = VAR_EMAIL_HOST_PASSWORD
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_SUBJECT_PREFIX = '[suventa]'
    PRODUCTION = True
    
except:
    pass

