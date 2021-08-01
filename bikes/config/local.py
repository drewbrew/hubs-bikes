import os
import sys

from .common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IN_TEST = sys.argv[1:2] == ["test"]


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

    if not IN_TEST:
        # Django overrides DEBUG to False in manage.py test by default
        INSTALLED_APPS = Common.INSTALLED_APPS + ("debug_toolbar",)
        MIDDLEWARE = (
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        ) + Common.MIDDLEWARE
        DEBUG_TOOLBAR_CONFIG = {
            "SHOW_TOOLBAR_CALLBACK": "bikes.toolbar_config.show_toolbar"
        }
