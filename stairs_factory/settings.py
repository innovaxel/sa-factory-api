"""
Django settings for stairs_factory project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path

from decouple import config
from decouple import Csv


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    "SECRET_KEY",
    "django-insecure-_sap-8=y7bvj9_g6^0w$7t!nbbntstjpsziq0%o%2yqa#pf&$",
)
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv())
CSRF_TRUSTED_ORIGINS = ["http://localhost:8100"]

INSTALLED_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts.apps.AccountsConfig",
    "jobs.apps.JobsConfig",
    "drf_yasg",
    "rest_framework_simplejwt.token_blacklist",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# AUTH_USER_MODEL = "accounts.SimpleUser"
# AUTH_USER_MODEL = "accounts.HumanResource"

AUTHENTICATION_BACKENDS = [
    "accounts.backends.HumanResourceBackend",
    # "django.contrib.auth.backends.ModelBackend",
]


ROOT_URLCONF = "stairs_factory.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "stairs_factory.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": "master",
        "USER": "sa",
        "PASSWORD": "Str0ngP@ssw0rd!",  # Correct key
        "HOST": "db",
        "PORT": "1433",
        "OPTIONS": {
            "driver": "ODBC Driver 17 for SQL Server",
            "extra_params": "TrustServerCertificate=yes;",
        },
    },
}

DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": "master",  # Use 'master' or the database you created
        "USER": "sa",  # Default MSSQL user
        "PASSWORD": "Str0ngP@ssw0rd!",  # Your MSSQL SA password
        "HOST": "sql_server",  # The service name of your MSSQL container in docker-compose
        "PORT": "1434",  # Host port mapped to 1433 in the container
        "OPTIONS": {
            "driver": "ODBC Driver 17 for SQL Server",  # Correct ODBC driver for MSSQL
            "extra_params": "TrustServerCertificate=yes;",  # Optional, helps with SSL
        },
    },
}


USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # "DEFAULT_PERMISSION_CLASSES": (
    #     "rest_framework.permissions.IsAuthenticated",
    # ),
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": config("JWT_HASHER"),
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# LOG_FILE_PATH_INFO = os.path.join(BASE_DIR, "logs", "info.log")
# LOG_FILE_PATH_ERROR = os.path.join(BASE_DIR, "logs", "error.log")

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "detailed": {
#             "format": (
#                 "[{levelname}] {asctime} {name} {threadName} {thread:d} "
#                 "{module} {filename} {lineno:d} {funcName} {message}"
#             ),
#             "style": "{",
#             "datefmt": "%Y-%m-%d %H:%M:%S",
#         },
#         "simple": {
#             "format": (
#                 "[{levelname}] {asctime} {name} {module} {filename} "
#                 "{lineno:d} {funcName} {message}"
#             ),
#             "style": "{",
#             "datefmt": "%Y-%m-%d %H:%M:%S",
#         },
#     },
#     "handlers": {
#         "file_info": {
#             "level": "INFO",
#             "class": "logging.FileHandler",
#             "filename": LOG_FILE_PATH_INFO,
#             "formatter": "detailed",
#         },
#         "file_error": {
#             "level": "ERROR",
#             "class": "logging.FileHandler",
#             "filename": LOG_FILE_PATH_ERROR,
#             "formatter": "detailed",
#         },
#         "console": {
#             "level": "INFO",
#             "class": "logging.StreamHandler",
#             "formatter": "simple",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["file_info", "file_error", "console"],
#             "level": "INFO",
#             "propagate": True,
#         },
#         "django.request": {
#             "handlers": ["file_info", "file_error", "console"],
#             "level": "WARNING",
#             "propagate": False,
#         },
#         "accounts": {
#             "handlers": ["file_info", "file_error", "console"],
#             "level": "DEBUG",
#             "propagate": False,
#         },
#         "jobs": {
#             "handlers": ["file_info", "file_error", "console"],
#             "level": "DEBUG",
#             "propagate": False,
#         },
#     },
# }
