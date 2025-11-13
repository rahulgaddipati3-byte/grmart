# shop/settings.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# Core / Environment
# =========================================================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key-change-me")
DEBUG = os.getenv("DEBUG", "True") == "True"

ON_RENDER = os.getenv("RENDER") == "1"
RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")  # e.g. "grmart.onrender.com"

if ON_RENDER:
    # Allow the Render hostname (and your fixed domain if you add one)
    ALLOWED_HOSTS = [h for h in [RENDER_HOST, "grmart.onrender.com"] if h]
    # CSRF must be exact origins (no wildcards)
    CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS]
else:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
    CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1", "http://localhost"]

# Make Django aware of HTTPS when behind Render’s proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Harden security when DEBUG=False
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24  # raise after verifying HTTPS works end-to-end
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False

# =========================================================
# Apps
# =========================================================
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
                "cart.context_processors.cart_count",

            ],
        },
    },
]

# =========================================================
# Database
# =========================================================
if ON_RENDER:
    # Use SQLite on Render, stored under a dedicated folder we create at startup.
    DATA_DIR = BASE_DIR / "data"
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": DATA_DIR / "db.sqlite3",
        }
    }
else:
    # Local MySQL (Workbench)
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

# =========================================================
# Static & Media
# =========================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]     # your repo assets (css/js/images used by templates)
STATIC_ROOT = BASE_DIR / "staticfiles"       # where collectstatic writes for production

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Let WhiteNoise also check STATICFILES_DIRS (so /static/css/neon.css works)
WHITENOISE_USE_FINDERS = True

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =========================================================
# Internationalization / Time
# =========================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================================================
# Auth redirects
# =========================================================
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"      # or "/products/"
LOGOUT_REDIRECT_URL = "/"

# =========================================================
# Email (dev)
# =========================================================
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@grmart.local"

# =========================================================
# Logging (simple & useful on Render)
# =========================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO" if ON_RENDER else "DEBUG"},
}
