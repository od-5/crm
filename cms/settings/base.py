import socket

__author__ = 'alexy'

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'u@5!he@8y6ynbta9c9(l=%b1qzb(c=*9*v)jf+1lkn%_by!jk*'

if socket.gethostname() == 'r420':
    DEBUG = True
else:
    DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'info@nadomofone.ru'
EMAIL_HOST = 'smtp.fullspace.ru'
EMAIL_HOST_USER = 'info@nadomofone.ru'
EMAIL_HOST_PASSWORD = 'alena2010'

ADMINS = (('Alexey', 'od-5@yandex.ru'),)

ROOT_URLCONF = 'cms.urls'

WSGI_APPLICATION = 'cms.wsgi.application'

AUTH_USER_MODEL = 'core.User'
LOGIN_URL = '/cabinet/login/'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, '../../django_cache'),
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}