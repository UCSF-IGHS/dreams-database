from .base import *

ALLOWED_HOSTS = ['*']
DEBUG = True

DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': 'db_unittest.sqlite3',
      }
}