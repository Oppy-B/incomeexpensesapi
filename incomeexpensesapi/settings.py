"""
Django settings for incomeexpensesapi project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import environ                                                   # NOTE :: IMPORTED THIS TO USE OUR HIDDEN PASSWORD CREDENTIALS
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sq-iyyu+fl8sn12e+1+x(myif)x$ix=g6ubx!kgq1d&3nl-lut'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'authentication.user'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',                                                 # NOTE :: STARTED ADDING APPS FROM HERE
    
    'drf_yasg',
    'authentication',
    'expenses',
    'income'
]

                                                                    # NOTE :: ADDING SWAGGER SETTING TO ALLOW US PROVIDE THE ACCESS
                                                                    # NOTE :: KEY FOR AUTHORISATION
SWAGGER_SETTINGS  = {
    'SECURITY_DEFINITIONS':{
        'Bearer': {
            'type' : 'apiKey',
            'name' : 'Authorization',
            'in' : 'header'
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'incomeexpensesapi.urls'

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

WSGI_APPLICATION = 'incomeexpensesapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK={                                                   # NOTE :: ADDED THIS TO CHANGE NONE-FIELD ERROR TO DISPLAY ERROR TO THE USER
    "NON_FIELD_ERRORS_KEY":"errors",
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,                                                # NOTE :: ADDED PAGINATION FROM THE RESTFRAMEWORK DOCUMENTATION


    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',      # NOTE :: MAKE SURE TO ADD THIS LINES OF CODE TO AVOID 
        'rest_framework.authentication.SessionAuthentication',    # GETTING AN ERROR THAT SAYS THIS "detail": "Authentication credentials were not provided."
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    
}
                                                                    # NOTE ADDED SIMPLEJWT HERE TO SPECIFY THE TOKE LIFETIME
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

                                                        # NOTE :: ADDED FRM HERE OUR CONFIGURATIONS TO SEND EMAILS

#Create an email to send the token for newly created user
'''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'authtest47'
#os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASWORD = 'Testing123$'
#os.environ.get('EMAIL_HOST_PASSWORD')

'''

"""
Note here that i am using the environ to protect my login credentials
step 1 : do a pip install environ
step 2 : import environ here in settings
step 3 : create a .env in the folder containing the settings.py file
step 4 : declare your environment varaibles in your .env file 
Then continue with the code below
Thanks!

"""
env = environ.Env()
environ.Env.read_env()

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
#'72eef0b9933536'
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD') 
#'b85702730386ba'
EMAIL_PORT = '2525'