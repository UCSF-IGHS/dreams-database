from .base import *

ALLOWED_HOSTS = ['*']
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dreams_test',
        'USER': 'dreams-django',
        'PASSWORD':"+3H'H%xfS92yQ:mZ",
        'HOST':'localhost',
        'PORT':'',
    }
}