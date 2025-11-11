# shop/settings.py
from pathlib import Path
import os

# =========================
# Paths
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# Security
# =========================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key-change-me")

# DEBUG is controlled by environment variable:
# - Locally you’ll usually have DEBUG=True (default below)
# - On Render we’ll set DEBUG=False
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".onrender.com",   # Render will use something like grmart.onrender.com
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]

# =========================
# Applications
# =========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # your apps
    "store",
    "cart",
    "orders",
    "accounts",
]

# =========================
# Middleware
# =========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "shop.urls"
WSGI_APPLICATION = "shop.wsgi.application"

# =========================
# Templates
# =========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # project-level templates (base.html, etc.)
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

# =========================
# Database
# =========================
# Use MySQL locally (DEBUG=True), SQLite on Render (DEBUG=False)
if DEBUG:
    # --- MySQL (Workbench) ---
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "grmart",               # same as in your SQL: USE grmart;
            "USER": "grmart_user",          # user you granted privileges to
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
else:
    # --- Simple SQLite for Render deployment ---
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# =========================
# Static & Media
# =========================
# Static files (CSS, JS, images)
STATIC_URL = "/static/"

# Where your custom CSS / images live in the repo
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Where collectstatic will put files for production
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media uploads (product images, etc.)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =========================
# Internationalization / timezone
# =========================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================
# Auth redirects
# =========================
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"      # after login go to welcome page
LOGOUT_REDIRECT_URL = "/"     # after logout go to welcome page

# =========================
# Email (dev: print to console)
# =========================
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@grmart.local"
