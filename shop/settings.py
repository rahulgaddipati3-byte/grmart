# shop/settings.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================
# Core
# ============================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key-change-me")

# Default DEBUG True locally; set DEBUG=False in Render env
DEBUG = os.getenv("DEBUG", "True") == "True"

# Detect Render
ON_RENDER = os.getenv("RENDER") == "1"
RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")  # Render sets this for your service

if ON_RENDER:
    # Prefer Render-provided hostname; fall back to your known domain
    ALLOWED_HOSTS = [h for h in [RENDER_HOST, "grmart.onrender.com"] if h]
    # Include exact origin(s) and wildcard for subdomains
    CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS] + ["https://*.onrender.com"]
else:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
    CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1", "http://localhost"]

# When behind Render’s proxy & in HTTPS, make Django aware
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Harden security automatically when DEBUG=False
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24  # 1 day (raise later if you like)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False

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
if ON_RENDER:
    # Simple & persistent: SQLite file in the Render disk
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "/var/data/db.sqlite3", 
        }
    }
else:
    # Local MySQL (your Workbench setup)
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

# Your repo static (e.g., css, images used by templates)
STATICFILES_DIRS = [BASE_DIR / "static"]

# Where collectstatic writes for production
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Let Whitenoise resolve files from STATICFILES_DIRS directly
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
LOGIN_REDIRECT_URL = "/"     # or "/products/"
LOGOUT_REDIRECT_URL = "/"

# ============================
# Email (dev)
# ============================
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@grmart.local"

# ============================
# Optional: basic logging
# ============================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO" if ON_RENDER else "DEBUG"},
}
