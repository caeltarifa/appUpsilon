"""
Django settings for appUpsilon_1 project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
######## BCRYPT PARA CIFRAR Y VALIDAR CONTRASEÑAS #########
#
#import bcrypt
#
###########################################################


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sb%@$i%e)zwtv=v_-p$^tc@%=%^kt7@becs*s0*m&tkhq^wp5c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['212.115.109.148','upsilon.aasana.ga', 'upsilon.aasana.bo']

GEOIP_PATH=os.path.join(BASE_DIR, 'geoip2')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.plan_vuelo',
    'apps.generacion_fpl',
    'apps.trabajadoresATS',
    'apps.aro_ais',
    'chartkick',
    'django_extensions'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'appUpsilon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'upsilon_template')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'template_tags': 'appUpsilon.templatetags.template_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'appUpsilon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
     'ENGINE': 'django.db.backends.postgresql_psycopg2',
     'NAME': 'upsilon_db', #nombre de la base de datos
	 'USER': 'postgres', #usuario de base de datos
	 'PASSWORD': 'nuclearaasana',
	 #'HOST': 'awsdatabase.clzuph1snvsw.eu-west-1.rds.amazonaws.com',

	 'HOST': '181.115.145.236',
	 #'HOST': 'upsilon2database.cyksvkkrkpzw.us-east-2.rds.amazonaws.com',
	 #'HOST': '54.217.136.199',
	 'PORT': 5432,
    },
    'aasana_bd': {
   #     'ENGINE': 'django.db.backends.sqlite3',
   #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

     'ENGINE': 'django.db.backends.postgresql_psycopg2',
     'NAME': 'boson_db', #nombre de la base de datos
         'USER': 'postgres', #usuario de base de datos
         'PASSWORD': 'nuclearaasana',
         'HOST': 'localhost',
         'PORT': 5432,
    },
}

DATABASE_ROUTERS = ['apps.trabajadoresATS.routers.MirrhhRouter',]


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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



################# LIBRERIAS PARA USAR ALGORITMOS DE CIFRAR PASSWORD ###############
#
#
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)
#
#
####################################################################################




# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL =  '/static/'

############################################################################################################
#                                   STATICFILES_DIRS                                                       #
#  la carpeta 'fotografias/' tiene acceso directo y esta vinculada a                                       #
#  la carpeta  /var/www/nuclear/appBoson/sistema_aasana/back-end/server/uploads/fotografias                #
#                                                                                                          #
############################################################################################################
import chartkick
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
    'fotografias/',
    chartkick.js() 
    )


# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

#LOGIN_REDIRECT_URL = '/plan_vuelo/admin'

MEDIA_URL = '/documents/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'documents')









# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },


    'applogfile': {
        'level':'DEBUG',
        'class':'logging.handlers.RotatingFileHandler',
        'filename': os.path.join('/logs/', 'APPNAME.log'),
        'maxBytes': 1024*1024*15, # 15MB
        'backupCount': 10,
    },


}



