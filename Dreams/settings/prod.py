from .base import *

ALLOWED_HOSTS = ['*']
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dreams_production',
        'USER': 'dreams-django',
        'PASSWORD':"+3H'H%xfS92yQ:mZ",
        'HOST':'localhost',
        'PORT':'3306',
    }
}

# Enable and disalbe running if fakedata through manage.py
GENERATE_FAKE_DATA = False
