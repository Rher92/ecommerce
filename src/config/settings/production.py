import os

import dj_database_url

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['rher92.pythonanywhere.com', 'mysterious-oasis-08740.herokuapp.com']

SECRET_KEY = os.environ.get('SECRET_KEY', default='foo')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

DATABASE_URL = os.environ.get("DATABASE_URL")
db_from_env = dj_database_url.config(
    default=DATABASE_URL, conn_max_age=500, ssl_require=True
)
DATABASES["default"].update(db_from_env)
