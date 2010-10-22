import platform
from unipath import FSPath as Path

BASE = Path(__file__).parent

DEBUG = TEMPLATE_DEBUG = platform.node() != 'jacobian.org'
MANAGERS = ADMINS = []

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False

DATABASES = {}
MIDDLEWARE_CLASSES = []

SITE_ID = 1
SECRET_KEY = 'b2@r_iu-3@#dm6+b2nt-iyu0n6#1j&!zt2a+3hw%9!_1k9!(2b'

ROOT_URLCONF = 'djangome.urls'
INSTALLED_APPS = ['djangome', 'gunicorn']
TEMPLATE_DIRS = [BASE.child('templates')]

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

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
        'django.request':{
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
