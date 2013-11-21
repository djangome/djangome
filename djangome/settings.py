import os
from unipath import FSPath as Path

BASE = Path(__file__).parent

DEBUG = TEMPLATE_DEBUG = 'DJANGO_DEBUG' in os.environ
MANAGERS = ADMINS = []

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False
WSGI_APPLICATION = 'scratch.wsgi.application'

DATABASES = {}
MIDDLEWARE_CLASSES = []

SITE_ID = 1
SECRET_KEY = os.environ['SECUREKEY'].split(',')[0]

ROOT_URLCONF = 'djangome.urls'
INSTALLED_APPS = ['djangome', 'gunicorn']
TEMPLATE_DIRS = [BASE.child('templates')]

REDIS_URL = os.environ['REDISCLOUD_URL']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

DJANGOME = {
    'VERSIONS': ['dev', '1.6', '1.5', '1.4', '1.3', '1.2', '1.1', '1.0'],
    'DEFAULT_VERSION': '1.6',
}
