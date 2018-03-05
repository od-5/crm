# coding=utf-8

LOCAL_SETTINGS = True
from settings import *


DEBUG = True

DEFAULT_FROM_EMAIL = 'info@nadomofone.ru'
EMAIL_HOST = 'smtp.fullspace.ru'
EMAIL_HOST_USER = 'info@nadomofone.ru'
EMAIL_HOST_PASSWORD = 'alena2010'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# settings for hosting
# DATABASES = {
#     'default': {
#          'ENGINE': 'django.db.backends.mysql',
#          'NAME': 'enjoyafrru_crm',
#          'USER': 'enjoyafrru_crm',
#          'PASSWORD': 'alena2010',
#          'HOST': 'localhost',
#          'PORT': '',
#      }
# }
