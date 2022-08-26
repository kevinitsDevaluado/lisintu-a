"""
Django settings for proyecto project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Paquete para variables de entorno .env
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = ')(m(t_vr2)cr%x(5vz7ordiyf-o*vv4b&tj$1-0jt#q3(vdf26'

SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
#python manage.py runserver 192.168.100.6:9595

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pwa',
    'apps.home',
    'apps.usuario',
    'apps.cliente',
    'apps.mantenimiento',
    'apps.bodega',
    'apps.publicidad',
    'apps.recordatorios',
]

#-------------- emails de pruebas ---------
INSTALLED_APPS += ('naomi',)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'proyecto.urls'

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

WSGI_APPLICATION = 'proyecto.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': config('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-EC'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# <----------------- Administrador ---------------->
# USER = admin
# PASS = admin-admin
#<----------------- Archivos staticos ---------------->
#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# <----------- Redireccion Login & LogOut ------------->

LOGIN_REDIRECT_URL = 'dashboard_index'
LOGOUT_REDIRECT_URL = '/'


# <----------------- Config Emails ---------------->
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('USER_MAIL')
EMAIL_HOST_PASSWORD = config('USER_MAIL_PASSWORD')
EMAIL_USE_TLS = True
#EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# <----------------- Testear correos ---------------->
# --------------------- ATENCION ---------------------
''' Crear en un directorio la carpeta tmp y
    cambiar en la variable EMAIL_FILE_PATH la ruta'''
if not DEBUG:
    EMAIL_BACKEND = "naomi.mail.backends.naomi.NaomiBackend"
    EMAIL_FILE_PATH = config('EMAIL_FILE_PATH')

# <------------- Configuracion para PWA --------------->

PWA_APP_NAME = "Corporación Pioneer Systems"
PWA_APP_DESCRIPTION = "PWA CPS"
PWA_APP_THEME_COLOR = "#040f28"
PWA_APP_BACKGROUND_COLOR = "#040f28"

PWA_APP_ICONS =[
    {
        "src":"/static/otros/img/logo_pwa.png",
        "sizes":"160x160"
    }
]

PWA_APP_ICONS_APPLE =[
    {
        "src":"/static/otros/img/logo_pwa.png",
        "sizes":"160x160"
    }
]

PWA_APP_SPLASH_SCREEN = [ 
    { 
        'src': '/static/otros/img/logo_pwa_sp.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, "serviceworker.js")