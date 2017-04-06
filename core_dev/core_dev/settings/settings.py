import sys

from .db import *
from .celery import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '#n$4rkjri9939y%=g6bf6=gh#p)4yo=##7-^fv=uw4(c-h5$%k'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'core_dev.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core_dev.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Atlantic/Reykjavik'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

DEBUG = True
ALLOWED_HOSTS = ['*']

if os.environ.get('DEBUG', 'false').lower() in ['1', 'true']:
    DEBUG_PROPAGATE_EXCEPTIONS = True
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(pathname)s:%(lineno)s: [%(levelname)s] %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'stream': sys.stdout,
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False
            },
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False
            },
        },
    }