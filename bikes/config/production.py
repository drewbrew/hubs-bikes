import os
import io

import environ
import google.auth
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import secretmanager

from .common import Common, BASE_DIR


env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")


try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
except DefaultCredentialsError:
    pass

if os.path.isfile(env_file):
    # Use a local secret file, if provided

    env.read_env(env_file)
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    env.read_env(io.StringIO(payload))
elif os.environ["DJANGO_CONFIGURATION"] == "Production":
    raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")


class Production(Common):
    if os.environ["DJANGO_CONFIGURATION"] == "Production":
        INSTALLED_APPS = Common.INSTALLED_APPS
        SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", env("SECRET_KEY"))

        DATABASES = {"default": env.db()}
        # Site
        # https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
        ALLOWED_HOSTS = ["*"]
        INSTALLED_APPS += ("gunicorn",)

        # Static files (CSS, JavaScript, Images)
        # https://docs.djangoproject.com/en/2.0/howto/static-files/
        # http://django-storages.readthedocs.org/en/latest/index.html
        INSTALLED_APPS += ("storages",)
        GS_BUCKET_NAME = env("GS_BUCKET_NAME")

        DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
        STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
        GS_DEFAULT_ACL = "publicRead"

        # https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/http-caching#cache-control
        # Response can be cached by browser and any intermediary caches (i.e. it is "public") for up to 1 day
        # 86400 = (60 seconds x 60 minutes x 24 hours)
        AWS_HEADERS = {
            "Cache-Control": "max-age=86400, s-maxage=86400, must-revalidate",
        }


if os.environ["DJANGO_CONFIGURATION"] == "Production" and os.getenv(
    "USE_CLOUD_SQL_AUTH_PROXY", None
):
    Production.DATABASES["default"]["HOST"] = "127.0.0.1"
    Production.DATABASES["default"]["PORT"] = 5432
