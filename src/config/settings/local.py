from .base import *  # noqa
import os

DEBUG = True
SECRET_KEY = '69!*pwk1w=9@lhnq^ctt5++-@15)&ibrebgw94xcd)%zz-w!$#'
ALLOWED_HOSTS = ["*"]
   
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
        'TEST': {
            'NAME': os.environ.get('POSTGRES_DB_TEST'),
        },        
    }
}