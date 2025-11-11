# shop/settings.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================
# Core
# ============================

# Use a real secret key in production (we pass it via env on Render)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key-change-me")

# DEBUG will be False on Render (set DEBUG=False there)
DEBUG = os.getenv("DEBUG", "True") == "True"

# Allowed hosts differ for local vs Render
if os.getenv("RENDER") == "1":
    ALLOWED_HOSTS = ["grmart.onrender.com"]
    # Needed for secure POSTs (login, signup, etc.) when DEBUG=False
    CSRF_TRUSTED_ORIGINS = ["https://grmart.onrender.com"]
else:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# ============================
# Apps
# ============================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # project apps
    "store",
    "cart",
    "orders",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "shop.urls"
WSGI_APPLICATION = "shop.wsgi.application"

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

# ============================
# Database
# ============================

# On Render (RENDER=1 in env) -> use SQLite file db.sqlite3
if os.getenv("RENDER") == "1":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # Local development -> your MySQL Workbench database
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "grmart",
            "USER": "grmart_user",
            "PASSWORD": "StrongPassword123",
            "HOST": "127.0.0.1",
            "PORT": "3306",
            "OPTIONS": {
                "charset": "utf8mb4",
                "use_unicode": True,
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

# ============================
# Static & Media
# ============================

STATIC_URL = "/static/"

# Where your neon.css, images, etc. live in the repo
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Where collectstatic puts files for production
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # Simpler: no manifest, just compressed static files
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Let Whitenoise use Django’s staticfiles finders (looks directly in STATICFILES_DIRS)
WHITENOISE_USE_FINDERS = True
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ============================
# Locale / Time
# ============================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================
# Auth redirects
# ============================

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"      # change to "/products/" if you want to land on products after login
LOGOUT_REDIRECT_URL = "/"

# ============================
# Email – dev (console)
# ============================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@grmart.local"
