from .settings import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ERP_development',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '192.168.13.91',
        'PORT': '3310',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []
