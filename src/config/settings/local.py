from .base import *  # noqa
from .base import *  # noqa


DEBUG = True
SECRET_KEY = '69!*pwk1w=9@lhnq^ctt5++-@15)&ibrebgw94xcd)%zz-w!$#'
ALLOWED_HOSTS = ["*"]
   
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce',
        'USER': 'ecommerce',
        'PASSWORD': 'ecommerce',
        'HOST': 'django-db',
        'PORT': 5432,
    }
}