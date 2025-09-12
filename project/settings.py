import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

assert os.getenv("SECRET_KEY") is not None and os.getenv("SECRET_KEY") != "", "SECRET_KEY is not set"
assert os.getenv("DB_NAME") is not None and os.getenv("DB_NAME") != "", "DB_NAME is not set"
assert os.getenv("DB_USER") is not None and os.getenv("DB_USER") != "", "DB_USER is not set"
assert os.getenv("DB_PORT") is not None and os.getenv("DB_PORT") != "", "DB_PORT is not set"
assert os.getenv("DB_HOST") is not None and os.getenv("DB_HOST") != "", "DB_HOST is not set"
assert os.getenv("DB_PASSWORD") is not None and os.getenv("DB_PASSWORD") != "", "DB_PASSWORD is not set"
assert (
    os.getenv("DEBUG") == "True"
    or (os.getenv("DEBUG") is None or os.getenv("DEBUG") == "False")
    and os.getenv("ALLOWED_HOSTS") is not None
    and os.getenv("ALLOWED_HOSTS") != ""
), "ALLOWED_HOSTS is not set when DEBUG=False"
assert (
    os.getenv("DEBUG") == "True"
    or (os.getenv("DEBUG") is None or os.getenv("DEBUG") == "False")
    and os.getenv("CUSTOMER_APP_ORIGIN") is not None
    and os.getenv("CUSTOMER_APP_ORIGIN") != ""
), "CUSTOMER_APP_ORIGIN is not set when DEBUG=False"

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False") == "True"

CORS_ALLOW_ALL_ORIGINS = DEBUG

ALLOWED_HOSTS = [] if DEBUG else os.getenv("ALLOWED_HOSTS").split(",")

CORS_ALLOWED_ORIGINS = [] if DEBUG else [os.getenv("CUSTOMER_APP_ORIGIN")]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = ["withauthentication", "content-type"]

APPEND_SLASH = False

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.accounts.apps.AccountsConfig",
    "apps.menu.apps.MenuConfig",
    "apps.orders.apps.OrdersConfig",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "apps.accounts.middlewares.RestrictApiAccessMiddleware",
    "apps.accounts.middlewares.JWTRefreshMiddleware",
    "apps.accounts.middlewares.JWTAuthMiddleware",
]

ROOT_URLCONF = "project.urls"

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

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "HOST": os.getenv("DB_HOST"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "PORT": int(os.getenv("DB_PORT")),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "apps.accounts.validators.CustomPasswordValidator",
    },
]

AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
}

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
