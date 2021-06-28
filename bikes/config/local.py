import os
from .common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True

    DATABASES = {
        "default": {
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "",
            "HOST": "postgres",
            "PORT": 5432,
            "CONN_MAX_AGE": 600,
            "ENGINE": "django.db.backends.postgresql_psycopg2",
        }
    }

    # Mail
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
