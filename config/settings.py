"""
Django settings for app project.

Generated by 'django-administrator startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

#INSTALANDO VARIABLES DE ENTORNO
import environ
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Set the project base directory
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env')) #Cambiar para produccion

# SECURITY WARNING: don't run with debug turned on in production!
# False if not in os.environ because of casting above
DEBUG = env('DEBUG')

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-pbfwo%(a1b4uu+1+4mhwm)$m7d64)^v9lx6$mg5qz0!k9pr5y8'
SECRET_KEY = env('SECRET_KEY')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/


ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#   'http://localhost:3000',
# )


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',

    #Libs Instaladas
    'rest_framework',
    'rest_framework_swagger',
    'django_seed',
    'django_q',
    'notifications',

    #Libs de Autenticacion
    'rest_framework.authtoken',
]
from helpers import AutoImporter
excludeApps = [
    'AppConfig',
]
INSTALLED_APPS += AutoImporter().loadApps(excludeApps)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    #Custom Middlewares
    'crum.CurrentRequestUserMiddleware'
]

ROOT_URLCONF = 'config.urls'

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
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            },
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR + '/database/db.sqlite3',
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cantera-joven-cujae',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.authentication.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.authentication.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.authentication.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.authentication.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es-cu'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authentication.DirectoryUser'

AUTHENTICATION_BACKENDS = [
    'custom.authentication.backend.DirectorioOnlineAuthBackend',#Autenticacion en Directorio Online
    'custom.authentication.backend.DirectorioLocalAuthBackend',#Autenticacion en Directorio Local
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.authentication` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_SCHEMA_CLASS':'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'custom.authentication.backend.APIKeyAuthentication',
        'custom.authentication.backend.BearerAuthentication'
    ),
}

SWAGGER_SETTINGS = {
    "exclude_url_names": ['doc_swagger'],
    "exclude_namespaces": ['admin','doc_swagger'],
    "SECURITY_DEFINITIONS":
        {
            'JWT': {'type':'apiKey','in':'header','name':'Auth JWT'},
            'Token': {'type':'apiKey','in':'header','name':'Auth Token'},
        },
    'USE_SESSION_AUTH':False
}

LOGGING = {
    'version': 1, #Version del Gestor de Registros
    'disable_existing_loggers': False, #Deshabilitar los registros predeterminados
    'handlers': { #Configurar los gestores
        'file':
            {
                'class': 'logging.FileHandler',
                'filename': 'registro.log',
                'formatter':'verbose'
            },
        'telegram':
            {
                'class':'custom.logging.TelegramLogHandler',
                'channel':env('TELEGRAM_CHANNEL'),
                'token':env('TELEGRAM_TOKEN'),
                'level':'ERROR',
                'formatter':'telegram-format',
            }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['file','telegram'],
        },
    },
    'formatters': { #Formatos del Log
        'verbose': {
            'format': '{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'telegram-format':{
            'class':'custom.logging.TelegramFormater'
        }
    },
}

Q_CLUSTER = {
    'name': 'CanteraJovenCUJAE',
    'workers':1,
    'timeout':60,
    'recycle':500,
    'compress':True,
    'queue_limit':500,
    'save_limit':250,
    'max_attempts':3,
    'label': 'Tareas de Cantera Joven CUJAE',
    'orm':'default'
}
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
#EMAIL_HOST = "smtp.gmail.com"
#EMAIL_PORT = 587
#EMAIL_HOST_USER = "staminainvestingoficial@gmail.com"
#EMAIL_HOST_PASSWORD = "uxgltkqrsrxwdjpw"
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '37b2ba9a1d8146'
EMAIL_HOST_PASSWORD = 'c8bfa6035e7dd0'
EMAIL_PORT = '2525'
