import os
from datetime import timedelta
from pathlib import Path
import environ
import toml
import logging

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(Path(__file__).joinpath(BASE_DIR, "secrets/.env"))

pyproject = toml.load(f"{BASE_DIR}/pyproject.toml")
API_VERSION = pyproject["tool"]["poetry"]["version"]

# Boring
ADMIN_USERNAME = env("ADMIN_USERNAME")
ADMIN_PASSWORD = env("ADMIN_PASSWORD")
ADMIN_EMAIL = env("ADMIN_EMAIL")
ADMINS = [(ADMIN_USERNAME, ADMIN_EMAIL)]
SITE_ID = 1
APP_URL = env("APP_URL", default="http://localhost")
AUTH_USER_MODEL = "core.CustomUser"

# Security
AUTH_PASSWORD_MIN_LENGTH: int = env.int("AUTH_PASSWORD_MIN_LENGTH", default=11)
ALLOWED_HOSTS: list[str] = env.list("ALLOWED_HOSTS", default=["*"])
CSRF_TRUSTED_ORIGINS: list[str] = env.list("CSRF_TRUSTED_ORIGINS")
PASSWORD_HASHERS = ["core.hashers.CustomArgon2PasswordHasher"]
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS: list[str] = env.list("CORS_ALLOWED_ORIGINS")


DEBUG: bool = env.bool("DEBUG")
SECRET_KEY: str = env.str("SECRET_KEY")
INTERNAL_IPS = ["127.0.0.1"]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "wsgi.application"
ASGI_APPLICATION = "asgi.application"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Local apps
    "core.apps.CoreConfig",
    "data.apps.DataConfig",
    "websocket.apps.WebsocketConfig",
    "event.apps.EventConfig",
    # Third party
    "corsheaders",
    "ninja",
    "ninja_jwt",
    "ninja_jwt.token_blacklist",
    "ninja_extra",
    # "nested_admin",
    # "django_celery_beat",
    "django_celery_results",
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

if DEBUG:
    INSTALLED_APPS += ["django_extensions"]

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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

# CELERY AND AUTOMATION
CELERY_BROKER_URL = env("REDIS_URL")

CELERY_TASK_DEFAULT_QUEUE = "default"
CELERY_TASK_DEFAULT_EXCHANGE = "default"
CELERY_TASK_DEFAULT_ROUTING_KEY = "default"
# CELERY_WORKER_CONCURRENCY = 2
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TASK_ALWAYS_EAGER = False
CELERY_ENABLE_UTC = True
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
CELERY_CACHE_BACKEND = "default"

CELERY_TIMEZONE = "UTC"
DJANGO_CELERY_BEAT_TZ_AWARE = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_CONNECTION_MAX_RETRIES = 5
CELERY_BROKER_CONNECTION_TIMEOUT = 10
CELERY_BROKER_HEARTBEAT = 30
CELERY_BROKER_HEARTBEAT_CHECKRATE = 3.0
CELERY_BROKER_POOL_LIMIT = 10
CELERY_WORKER_PREFETCH_MULTIPLIER = 1

CELERY_BROKER_TRANSPORT_OPTIONS = {
    "queue_max_priority": 10,
    "visibility_timeout": 3600,
    "fanout_prefix": True,
    "fanout_patterns": True,
}

CELERY_TASK_RESULT_EXPIRES = 86400
CELERY_TASK_DEFAULT_DELIVERY_MODE = "persistent"
CELERY_TASK_DEFAULT_PRIORITY = 0

CELERY_TASK_DEFAULT_ANNOTATIONS = {
    "retries": 3,
    "rate_limit": "100/s",
}
CELERY_TASK_DEFAULT_TIME_LIMIT = 60
CELERY_TASK_DEFAULT_SOFT_TIME_LIMIT = 60
CELERY_TASK_DEFAULT_MAX_RETRIES = 3
CELERY_TASK_DEFAULT_RETRY_DELAY = 60
CELERY_TASK_DEFAULT_RETRY_BACKOFF = True

CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERY_WORKER_LOG_FORMAT = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
CELERY_WORKER_TASK_LOG_FORMAT = "[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s"

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

# openssl ecparam -name secp521r1 -genkey -noout -out private_key.pem
# openssl ec -in private_key.pem -pubout -out public_key.pem
with open(os.path.join(BASE_DIR, "secrets", "private_key.pem")) as f:
    PRIVATE_KEY: str = f.read()

with open(os.path.join(BASE_DIR, "secrets", "public_key.pem")) as f:
    PUBLIC_KEY: str = f.read()

NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "ES512",
    "SIGNING_KEY": PRIVATE_KEY,
    "VERIFYING_KEY": PUBLIC_KEY,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "ninja_jwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("ninja_jwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "ninja_jwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "TOKEN_OBTAIN_PAIR_INPUT_SCHEMA": "ninja_jwt.schema.TokenObtainPairInputSchema",
    "TOKEN_OBTAIN_PAIR_REFRESH_INPUT_SCHEMA": "ninja_jwt.schema.TokenRefreshInputSchema",
    "TOKEN_BLACKLIST_INPUT_SCHEMA": "ninja_jwt.schema.TokenBlacklistInputSchema",
    "TOKEN_VERIFY_INPUT_SCHEMA": "ninja_jwt.schema.TokenVerifyInputSchema",
}

NINJA_EXTRA = {
    "PAGINATION_CLASS": "ninja_extra.pagination.PageNumberPaginationExtra",
    "PAGINATION_PER_PAGE": 100,
    "INJECTOR_MODULES": [],
    "THROTTLE_CLASSES": [
        "ninja_extra.throttling.AnonRateThrottle",
        "ninja_extra.throttling.UserRateThrottle",
    ],
    "THROTTLE_RATES": {
        "user": "1000/day",
        "anon": "100/day",
    },
    "NUM_PROXIES": None,
    "ORDERING_CLASS": "ninja_extra.ordering.Ordering",
    "SEARCHING_CLASS": "ninja_extra.searching.Search",
}

# wide_console = Console(width=200)
# logging.basicConfig(
#     level="INFO",
#     handlers=[RichHandler(console=wide_console, rich_tracebacks=True, markup=True)],
#     format="%(asctime)s %(levelname)s %(name)s %(message)s " "[PID:%(process)d:%(threadName)s]",
# )
#
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "root": {"level": "INFO", "handlers": ["rich", "access_file"]},
#     "formatters": {
#         "rich": {
#             "datefmt": "[%X]",
#             "format": "%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s",
#             # " "[PID:%(process)d:%(threadName)s]",
#         },
#         "verbose": {
#             "format": "%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s",
#             # " "[PID:%(process)d:%(threadName)s]",
#         },
#     },
#     "handlers": {
#         "rich": {
#             "class": "rich.logging.RichHandler",
#             "formatter": "rich",
#             "level": "INFO",
#             "rich_tracebacks": True,
#             "markup": True,
#             "console": wide_console,
#         },
#         "access_file": {
#             "level": "INFO",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": "logs/access.log",
#             "maxBytes": 1024 * 1024 * 5,
#             "backupCount": 5,
#             "formatter": "verbose",
#         },
#         "error_file": {
#             "level": "ERROR",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": "logs/error.log",
#             "maxBytes": 1024 * 1024 * 5,
#             "backupCount": 5,
#             "formatter": "verbose",
#         },
#         "celery_file": {
#             "level": "INFO",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": "logs/celery.log",
#             "maxBytes": 1024 * 1024 * 5,
#             "backupCount": 5,
#             "formatter": "verbose",
#         },
#     },
#     "loggers": {
#         "uvicorn.access": {
#             "handlers": ["rich", "access_file"],
#             "level": "INFO",
#             "propagate": False,
#         },
#         "uvicorn.error": {
#             "handlers": ["rich", "error_file"],
#             "level": "ERROR",
#             "propagate": False,
#         },
#         "django": {
#             "handlers": ["rich", "access_file", "error_file"],
#             "level": "INFO",
#             "propagate": False,
#         },
#         "celery.app.trace": {
#             "handlers": ["rich", "celery_file"],
#             "level": "INFO",
#             "propagate": False,
#         },
#         "celery.task": {
#             "handlers": ["rich", "celery_file"],
#             "level": "INFO",
#             "propagate": False,
#         },
#     },
# }
# wide_console = Console(width=200)
#
# logging.basicConfig(
#     level="INFO",
#     handlers=[RichHandler(console=wide_console, rich_tracebacks=True, markup=True)],
#     format="%(asctime)s %(levelname)s %(name)s %(message)s " "[PID:%(process)d:%(threadName)s]",
# )

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "root": {"level": "INFO", "handlers": ["console"]},
#     "formatters": {
#         "rich": {
#             "datefmt": "[%X]",
#             "format": "%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s",
#         },
#         "verbose": {
#             "format": "%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s",
#         },
#     },
#     "handlers": {
#         # Console handler for terminal output
#         "console": {
#             "class": "rich.logging.RichHandler",
#             "formatter": "rich",
#             "level": "INFO",
#             "rich_tracebacks": True,
#             "markup": True,
#             "console": wide_console,
#         },
#         # File handler for Django logs
#         "django_file": {
#             "level": "INFO",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": "logs/django.log",
#             "maxBytes": 1024 * 1024 * 5,
#             "backupCount": 5,
#             "formatter": "verbose",
#         },
#         # File handler for Celery logs
#         "celery_file": {
#             "level": "INFO",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": "logs/celery.log",
#             "maxBytes": 1024 * 1024 * 5,
#             "backupCount": 5,
#             "formatter": "verbose",
#         },
#     },
#     "loggers": {
#         # Logger for Django
#         "django": {
#             "handlers": ["console", "django_file"],
#             "level": "INFO",
#             "propagate": False,
#         },
#         # Logger for Celery
#         "celery": {
#             "handlers": ["console", "celery_file"],
#             "level": "INFO",
#             "propagate": False,
#         },
#         # Celery task-specific logger
#         "celery.task": {
#             "handlers": ["console", "celery_file"],
#             "level": "INFO",
#             "propagate": False,
#         },
#     },
# }
