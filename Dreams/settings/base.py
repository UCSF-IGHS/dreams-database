# coding=utf-8
"""
Django settings for Dreams project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True   # Changed to False for custom error messaging!

ALLOWED_HOSTS = ['127.0.0.1', '*']

# Application definition
PREREQ_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
    'ckeditor',
    'ckeditor_uploader',
    'widget_tweaks'
]

PROJECT_APPS = [
    'rest_framework',
    'xf.xf_crud',
    'xf.xf_system',
    'xf.uc_dashboards',
    'crispy_forms',
    'xf.uc_dashboards.templatetags.getattribute',
    'xf.uc_dashboards.templatetags.dashgent_filters',
    'xf.uc_dashboards.templatetags.iif',
    'Dreams',
    'DreamsApp',
]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'DreamsApp.middlewares.AutoLogoutMiddleware.SessionExpiredMiddleware',
    'DreamsApp.middlewares.CurrentUserMiddleware.CurrentUserMiddleware',
]

ROOT_URLCONF = 'Dreams.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../templates')],
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

WSGI_APPLICATION = 'Dreams.wsgi.application'

DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
      }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
SESSION_EXPIRY_AGE = 20 # This is in Minutes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "../static")

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    'DreamsApp',
)

# Fixture dir. Contains path to json file used at migration
# Use manage.py loaddata fixture-name
# e.g manage.py loaddata initial_data.json
FIXTURE_DIRS = ()

MEDIA_ROOT = '/media/'
MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = ''
CKEDITOR_JQUERY_URL = os.path.join(STATIC_URL, 'gla/vendors/jquery/dist/jquery.min.js')
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'skin': 'moono-lisa',
        'width': '100%'
    },
}

gettext = lambda s: s

LANGUAGES = (
    ('en-gb', gettext('English')),
    ('pt', gettext('Portuguese')),
    ('nl', gettext('Dutch')),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en-gb'

LANGUAGE_COOKIE_NAME = "lc"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'NOTSET',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'NOTSET',
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO'
        }
    }
}

# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    "DATE_INPUT_FORMATS": ["%d-%m-%Y", "%Y-%m-%d"],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
