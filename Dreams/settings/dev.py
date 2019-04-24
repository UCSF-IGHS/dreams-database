from .base import *

ALLOWED_HOSTS = ['*']
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dreams_dev',
        'USER': 'dreams-django',
        'PASSWORD':"+3H'H%xfS92yQ:mZ",
        'HOST':'localhost',
        'PORT':'3306',
    }
}