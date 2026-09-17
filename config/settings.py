import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# ENVIRONMENT
# --------------------------------------------------

load_dotenv(BASE_DIR / ".env")


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "DJANGO_SECRET_KEY is missing. "
        "Add it to your .env file or production environment."
    )


DEBUG = os.getenv(
    "DJANGO_DEBUG",
    "False",
).lower() in (
    "1",
    "true",
    "yes",
    "on",
)


SITE_URL = os.getenv(
    "SITE_URL",
    "https://thebereanscale.com",
).rstrip("/")


# --------------------------------------------------
# HOSTS
# --------------------------------------------------

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        ("127.0.0.1," "localhost," "thebereanscale.com," "www.thebereanscale.com"),
    ).split(",")
    if host.strip()
]


RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")


if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


CSRF_TRUSTED_ORIGINS = [
    "https://thebereanscale.com",
    "https://www.thebereanscale.com",
]


if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")


# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "storages",
    "blog",
]


# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------

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


ROOT_URLCONF = "config.urls"


# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": ("django.template.backends.django.DjangoTemplates"),
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                ("django.template.context_processors.request"),
                ("django.contrib.auth." "context_processors.auth"),
                ("django.contrib.messages." "context_processors.messages"),
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")


if DATABASE_URL:

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

else:

    DATABASES = {
        "default": {
            "ENGINE": ("django.db.backends.sqlite3"),
            "NAME": (BASE_DIR / "db.sqlite3"),
        }
    }


# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth."
            "password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth." "password_validation." "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth." "password_validation." "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth." "password_validation." "NumericPasswordValidator"
        ),
    },
]


# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_TZ = True


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# --------------------------------------------------
# CLOUDFLARE R2
# --------------------------------------------------

R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")

R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")

R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")

R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL")

R2_PUBLIC_DOMAIN = os.getenv("R2_PUBLIC_DOMAIN")


USE_R2 = all(
    [
        R2_ACCESS_KEY_ID,
        R2_SECRET_ACCESS_KEY,
        R2_BUCKET_NAME,
        R2_ENDPOINT_URL,
        R2_PUBLIC_DOMAIN,
    ]
)


# --------------------------------------------------
# STORAGE
# --------------------------------------------------

if USE_R2:

    STORAGES = {
        "default": {
            "BACKEND": ("storages.backends.s3." "S3Storage"),
            "OPTIONS": {
                "access_key": (R2_ACCESS_KEY_ID),
                "secret_key": (R2_SECRET_ACCESS_KEY),
                "bucket_name": (R2_BUCKET_NAME),
                "endpoint_url": (R2_ENDPOINT_URL),
                "region_name": "auto",
                "signature_version": ("s3v4"),
                "default_acl": None,
                "file_overwrite": False,
                "querystring_auth": False,
                "custom_domain": (R2_PUBLIC_DOMAIN),
                "url_protocol": "https:",
            },
        },
        "staticfiles": {
            "BACKEND": ("whitenoise.storage." "CompressedManifestStaticFilesStorage"),
        },
    }

else:

    STORAGES = {
        "default": {
            "BACKEND": ("django.core.files.storage." "FileSystemStorage"),
        },
        "staticfiles": {
            "BACKEND": ("whitenoise.storage." "CompressedManifestStaticFilesStorage"),
        },
    }


# --------------------------------------------------
# LOCAL MEDIA
# --------------------------------------------------

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# --------------------------------------------------
# SECURITY
# --------------------------------------------------

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


if not DEBUG:

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = "DENY"

else:

    SECURE_SSL_REDIRECT = False


# --------------------------------------------------
# DEFAULT PRIMARY KEY
# --------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
