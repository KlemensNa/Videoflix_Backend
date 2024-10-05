"""
Django settings for filmflix_backend project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import environ
import os
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
import sys

# Überprüfe, ob die Tests ausgeführt werden
# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': lambda request: False if 'test' in sys.argv else True,
# }



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    "sportflix.naueka.de"
]

INTERNAL_IPS = [
    "127.0.0.1",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "https://sportflix.naueka.de"
]

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    # andere erlaubte Header
]

CORS_ALLOW_CREDENTIALS = True

CACHETTL = getattr(settings, 'CACHETTL', DEFAULT_TIMEOUT)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_safe_settings',
    'rest_framework',
    'rest_framework.authtoken',
    'filmflix.apps.FilmflixConfig',
    "corsheaders",
    'import_export',
    'django_rq',
]

# if DEBUG:
#     INSTALLED_APPS += [
#         'debug_toolbar',
#     ]    

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',    
]

# if DEBUG:
#     MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'filmflix_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'filmflix_backend.wsgi.application'


# Databases
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

#SQLite
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

#local PostgreSQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': env('DB_NAME_LOCAL'),
#         'USER': env('DB_USER_LOCAL'),
#         'PASSWORD': env('DB_PASSWORD_LOCAL'),
#         'PORT': env('DB_PORT_LOCAL'),
#         'HOST': env('DB_HOST_LOCAL'),        
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'PORT': env('DB_PORT'),
        'HOST': env('DB_HOST'),
        'TEST': {
            'NAME': 'test_filmflix',  # Testdatenbankname
        },      
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/staticfiles')

IMPORT_EXPORT_USE_TRANSACTIONS = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "filmflix.CustomerUser"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [       
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',        
    ]
}


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = 'media/'

CACHES = {    
          "default": {        
              "BACKEND": "django_redis.cache.RedisCache",        
              "LOCATION": "redis://127.0.0.1:6379/1",        
              "OPTIONS": {     
                  'PASSWORD': 'foobared',       
                  "CLIENT_CLASS": "django_redis.client.DefaultClient"        },        
              "KEY_PREFIX": "videoflix"    }
          }


#change password in redis.config "requirepass"
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': 'foobared',
        'DEFAULT_TIMEOUT': 360,
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = True 
EMAIL_USE_SSL = False
EMAIL_HOST_USER = env('EMAIL_HOST_USER')  
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')          
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')


# CSRF_COOKIE_SECURE = True  # CSRF nur über HTTPS senden
# SESSION_COOKIE_SECURE = True  # Session-Cookies nur über HTTPS
# SECURE_SSL_REDIRECT = True  # Weiterleitung von HTTP auf HTTPS
# SECURE_HSTS_SECONDS = 3600  # HTTP Strict Transport Security (HSTS)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

