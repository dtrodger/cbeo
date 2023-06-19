"""
Django Application Configuration
"""
import os
import pathlib

from utils import get_env_var
from apps.core.apis.sentry import configure_sentry


ENVIRONMENT = get_env_var("ENVIRONMENT")
VERSION = get_env_var("VERSION")
configure_sentry(ENVIRONMENT, VERSION)
BASE_DIR = pathlib.Path()
ALLOWED_HOSTS = get_env_var("ALLOWED_HOSTS", is_list=True)
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
AWS_S3_CDN = get_env_var("AWS_S3_CDN", is_bool=True)
if AWS_S3_CDN:
    AWS_ACCESS_KEY_ID = get_env_var("AWS_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = get_env_var("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = get_env_var("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
else:
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_URL = "/mediafiles/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

ENV_FILE_PATH = os.path.join(BASE_DIR, ".env")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": get_env_var("CACHE_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "DB": get_env_var("CACHE_DB", is_int=True),
            "CONNECTION_POOL_CLASS_KWARGS": {
                "max_connections": get_env_var("CACHE_MAX_CONNECTIONS", is_int=True),
                "timeout": get_env_var("CACHE_CONNECTION_POOL_TIMEOUT", is_int=True),
            },
            "MAX_CONNECTIONS": get_env_var("CACHE_MAX_CONNECTIONS", is_int=True),
        },
    }
}
CORS_ALLOWED_ORIGINS = get_env_var("CORS_ALLOWED_ORIGINS", is_list=True)
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_env_var("DB_NAME"),
        "USER": get_env_var("DB_USER"),
        "PASSWORD": get_env_var("DB_PASSWORD"),
        "PORT": get_env_var("DB_PORT"),
        "HOST": get_env_var("DB_HOST"),
    }
}
DEBUG = get_env_var("DEBUG", is_bool=True)
INSTALLED_APPS = (
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "rest_framework",
    "corsheaders",
    "django_extensions",
    "storages",
    "django_filters",
    # Custom
    "apps.core",
)
INTERNAL_IPS = get_env_var("INTERNAL_IPS", is_list=True)
REQUEST_LOGGING = get_env_var("REQUEST_LOGGING", is_bool=True)
MIDDLEWARE = [
    "apps.core.middleware.LoggingMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
ROOT_URLCONF = "urls"
SECRET_KEY = get_env_var("SECRET_KEY")
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]
TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.request",)
WSGI_APPLICATION = "wsgi.application"
LANGUAGE_CODE = "en-us"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "stdout": {"class": "logging.StreamHandler", "formatter": "standard"},
        "info_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "standard",
            "filename": "logs/info.log",
            "mode": "a",
            "maxBytes": 1048576,
            "backupCount": 1,
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "standard",
            "filename": "logs/error.log",
            "mode": "a",
            "maxBytes": 1048576,
            "backupCount": 1,
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {
            "handlers": ["stdout", "info_file", "error_file"],
            "level": "DEBUG",
        },
        "gunicorn": {
            "level": "INFO",
            "handlers": ["stdout", "info_file", "error_file"],
        },
        "urllib3": {
            "handlers": ["stdout", "info_file", "error_file"],
            "level": "ERROR",
        },
        "botocore": {
            "handlers": ["stdout", "info_file", "error_file"],
            "level": "ERROR",
        },
        "boto3": {"handlers": ["stdout", "info_file", "error_file"], "level": "ERROR"},
        "sentry_sdk": {
            "handlers": ["stdout", "info_file", "error_file"],
            "level": "INFO",
        },
    },
}
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = False
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}
