"""
Django settings for user_manager_sys project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-%by6t_r05zgq%2sp_g(bxc)04e8yftnw7roe@#akphd9wn78h9",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True)

IS_PRODUCTION = config("IS_PRODUCTION", default=False)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=list, default=["*"])


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "manager",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

if DEBUG:
    # Doc django_bootstrap5: https://django-bootstrap5.readthedocs.io/en/latest/
    INSTALLED_APPS += [
        "django_browser_reload",
        "django_bootstrap5",
    ]
    MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]


ROOT_URLCONF = "user_manager_sys.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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

WSGI_APPLICATION = "user_manager_sys.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


if config("RUNIN_IN_CONTAINER", default=False, cast=bool):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("POSTGRES_NAME"),
            "USER": config("POSTGRES_USER"),
            "PASSWORD": config("POSTGRES_PASSWORD"),
            "HOST": config("POSTGRES_HOST"),
            "PORT": config("POSTGRES_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_DIRS = [BASE_DIR / "static"]

STATIC_URL = "static/"

MEDIA_URL = "media/"

STATIC_ROOT = "staticfiles"

MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        "LOCATION": STATIC_ROOT,
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "LOCATION": MEDIA_ROOT,
    },
    "s3": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "ACCESS_KEY_ID": config("ACCESS_KEY_ID", default=""),
        "SECRET_ACCESS_KEY": config("SECRET_ACCESS_KEY", default=""),
        "AWS_STORAGE_BUCKET_NAME": config("AWS_STORAGE_BUCKET_NAME", default=""),
        "AWS_S3_REGION_NAME": config("AWS_S3_REGION_NAME", default=""),
        "AWS_DEFAULT_ACL": config("AWS_DEFAULT_ACL", default=""),
        "AWS_S3_FILE_OVERWRITE": False,
    },
}


# Login and logout configs

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/index/"

LOGOUT_REDIRECT_URL = "/login/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "manager.CustomUserModel"
