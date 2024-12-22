from pathlib import Path
import environ

# jesus christ
api_folder = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(Path(__file__).joinpath(api_folder, "secrets/.env"))

API_VERSION = "0.1.04"

# Boring
BASE_DIR = Path(__file__).resolve().parent.parent
ADMIN_USERNAME = env("ADMIN_USERNAME")
ADMIN_PASSWORD = env("ADMIN_PASSWORD")
ADMIN_EMAIL = env("ADMIN_EMAIL")
ADMINS = [(ADMIN_USERNAME, ADMIN_EMAIL)]
SITE_ID = 1
APP_URL = env("APP_URL", default="http://localhost")


# Security
AUTH_PASSWORD_MIN_LENGTH: int = env.int("AUTH_PASSWORD_MIN_LENGTH", default=11)
ALLOWED_HOSTS: list[str] = env.list("ALLOWED_HOSTS", default=["*"])
CSRF_TRUSTED_ORIGINS: list[str] = env.list("CSRF_TRUSTED_ORIGINS")
# PASSWORD_HASHERS = ["core.hashers.CustomArgon2PasswordHasher"]
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS: list[str] = env.list("CORS_ALLOWED_ORIGINS")


# Soy
DEBUG: bool = env.bool("DEBUG")
SECRET_KEY: str = env.str("SECRET_KEY")

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "wsgi.application"
ASGI_APPLICATION = "asgi.application"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


INTERNAL_IPS = ["127.0.0.1"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core.apps.CoreConfig",
    # "corsheaders",
    "ninja",
    # "ninja_jwt",
    # "ninja_jwt.token_blacklist",
    # "ninja_extra",
    # "nested_admin",
    # "django_celery_beat",
    # "django_celery_results",
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

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": AUTH_PASSWORD_MIN_LENGTH},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

DATABASES = {"default": env.db("DATABASE_URL")}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = f"{APP_URL}/media/"
MEDIA_ROOT = BASE_DIR / "media"
STATICFILES_DIRS = [BASE_DIR / "extra_static"]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {"location": BASE_DIR / "media", "base_url": MEDIA_URL},
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        "OPTIONS": {"location": BASE_DIR / "static", "base_url": STATIC_URL},
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
