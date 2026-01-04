# settings.py
import sys
sys.stdout.reconfigure(encoding='utf-8')

import pymysql
pymysql.install_as_MySQLdb()

from pathlib import Path
import os
from dotenv import load_dotenv

# ======================
# BASE
# ======================

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ======================
# ENV
# ======================

DJANGO_ENV = os.getenv("DJANGO_ENV", "development")
DEBUG = os.getenv("DEBUG", "False") == "True"


import logging
logger = logging.getLogger(__name__)
logger.info("Loaded settings for %s environment. DEBUG=%s", DJANGO_ENV, DEBUG)

# ======================
# SECURITY
# ======================

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-dev-key")

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://*.ngrok-free.dev",
    "https://new-bombay.onrender.com"
]



# ======================
# IMAGEKIT
# ======================

IMAGEKIT_PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY")
IMAGEKIT_PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY")
IMAGEKIT_URL_ENDPOINT = os.getenv("IMAGEKIT_URL_ENDPOINT")

# ======================
# APPS
# ======================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "store",
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

ROOT_URLCONF = "Auto_mobile.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "Auto_mobile.wsgi.application"

# ======================
# DATABASE CONFIG
# ======================

if DJANGO_ENV == "production":
    # 🔵 PRODUCTION → TiDB Cloud
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT", "4000"),
            "OPTIONS": {
                "ssl": {"ssl": {}},
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    # 🟢 LOCAL → SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ======================
# PASSWORDS
# ======================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ======================
# I18N
# ======================

LANGUAGE_CODE = "en-us"
TIME_ZONE = 'Asia/Kolkata'
USE_TZ = True
USE_I18N = True


# ======================
# STATIC & MEDIA
# ======================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ======================
# AUTH
# ======================

LOGIN_URL = "staff_login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "dashboard"

X_FRAME_OPTIONS = "SAMEORIGIN"


print(f"⚙️⚙️⚙️  {DJANGO_ENV} ⚙️⚙️⚙️. DEBUG={DEBUG}")