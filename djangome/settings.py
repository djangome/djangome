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
WSGI_APPLICATION = 'djangome.wsgi.application'
STATIC_URL = '/static/'

try:
    from local_settings import DATABASES
except ImportError:
    import dj_database_url
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config()

SITE_ID = 1

_securekey_var = next(k for k in os.environ if k.startswith('SECUREKEY'))
SECRET_KEY = os.environ[_securekey_var].split(',')[0]


ROOT_URLCONF = 'djangome.urls'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'djangome', 
    'gunicorn'
]
TEMPLATE_DIRS = [BASE.child('templates')]

_redis_var = next(k for k in os.environ if k.startswith('REDIS'))
REDIS_URL = os.environ[_redis_var]

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
