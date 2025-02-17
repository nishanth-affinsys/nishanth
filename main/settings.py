import ast
import csv
import logging.config
import os
import sys
from pathlib import Path

from pubsub import PubSub as NatsPubSub
from kombu_client import PubSub as KombuPubSub
import boto3
from django.core.exceptions import ImproperlyConfigured
from django.core.management.utils import get_random_secret_key
from django.utils.log import DEFAULT_LOGGING

from main.log_config import get_logger_config_with_file, get_logger_config_without_file
import oracledb

oracledb.version = "8.3.0"
sys.modules["cx_Oracle"] = oracledb

from django.db.backends.oracle.base import DatabaseOperations

DatabaseOperations.max_name_length = lambda s: 128


def get_env_value(env_variable):
    try:
        return os.environ[env_variable]
    except KeyError as e:
        error_msg = f"Set the {env_variable} environment variable"
        raise ImproperlyConfigured(error_msg) from e


def get_int_env_value(env_variable):
    try:
        return int(os.environ[env_variable])
    except KeyError as e:
        error_msg = f"Set the {env_variable} environment variable"
        raise ImproperlyConfigured(error_msg) from e


def get_boolean_env_value(env_variable):
    try:
        return os.environ[env_variable] == "True"
    except KeyError as e:
        error_msg = f"Set the {env_variable} environment variable"
        raise ImproperlyConfigured(error_msg) from e


def get_array_like_env(env_variable, allowed_values=None):
    env_array = [
        env_item.strip()
        for env_item in os.environ[env_variable].split(",")
        if env_item.strip()
    ]

    if allowed_values is not None:
        env_array = [env_item for env_item in env_array if env_item in allowed_values]

    return env_array


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE Directory Variable
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_boolean_env_value("DEBUG")

ALLOWED_HOSTS = get_array_like_env("ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    "api_request_logging",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "rest_framework",
    "drf_spectacular",
    "drf_standardized_errors",
    "handoff",
    "console",
    "clickstream",
    "campaign_manager",
    "onboarding",
    "client_specific",
    "complaints",
    "vision",
    "profile_data",
    "metadata",
    "wallet",
    "pika_client",
    "scheduler",
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    "NON_FIELD_ERRORS_KEY": None,
    "DEFAULT_AUTHENTICATION_CLASSES": ["auth.authentication.BBAuth"],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Boilerplate  1.x",
    "DESCRIPTION": "",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
}

MIDDLEWARE = [
    # "api_request_logging.middleware.APILoggingMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "main.tenant_middleware.TenantMiddleware",
]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [f'{BASE_DIR}{get_env_value("TEMPLATE_PATH")}'],
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

WSGI_APPLICATION = "main.wsgi.application"
ASGI_APPLICATION = "main.routing.application"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = get_env_value("LANGUAGE_CODE")

TIME_ZONE = get_env_value("TIME_ZONE")

USE_I18N = get_boolean_env_value("USE_I18N")

USE_L10N = get_boolean_env_value("USE_L10N")

USE_TZ = get_boolean_env_value("USE_TZ")
# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Databases

# Initially Database will be empty in order to configure it with various database backends

DATABASES = {}
db_engine_postgres = "django.db.backends.postgresql"
db_engine_oracle = "django.db.backends.oracle"
db_engine_sqlite = "django.db.backends.sqlite3"
DB_ENGINE = (
    "postgres"
    if get_env_value("DB_ENGINE_default") in ["postgres_schema", "postgres_schema_ssl"]
    else (
        "oracle"
        if ["oracle_easy_connect", "oracle_full_connect", "oracle"]
        else "sqlite"
    )
)


def add_database_config_for_sqlite(tenant):
    DATABASES[tenant] = {
        "ENGINE": db_engine_sqlite,
        "NAME": os.path.join(BASE_DIR, f"{tenant}.sqlite3"),
    }


def add_database_config_for_postgres_schema(tenant):
    host = get_env_value(f"POSTGRES_DB_HOST_{tenant}")
    port = get_env_value(f"POSTGRES_DB_PORT_{tenant}")
    name = get_env_value(f"POSTGRES_DB_NAME_{tenant}")
    user = get_env_value(f"POSTGRES_DB_USER_{tenant}")
    password = get_env_value(f"POSTGRES_DB_PASSWORD_{tenant}")
    if "test" in sys.argv:
        DATABASES[tenant] = {
            "ENGINE": db_engine_postgres,
            "HOST": host,
            "PORT": port,
            "NAME": name,
            "USER": user,
            "PASSWORD": password,
            "OPTIONS": {"options": f"-c search_path={get_env_value(f'DB_SCHEMA_{tenant}')}"
                        },
            'TEST': {
                'MIRROR': 'default',  # This tells Django to use the same database without creating a test database
            }
        }
    else:
        DATABASES[tenant] = {
            "ENGINE": db_engine_postgres,
            "HOST": host,
            "PORT": port,
            "NAME": name,
            "USER": user,
            "PASSWORD": password,
            "OPTIONS": {
                "options": f"-c search_path={get_env_value(f'DB_SCHEMA_{tenant}')}"
            },
        }


def add_database_config_for_postgres_schema_with_ssl(tenant):
    host = get_env_value("POSTGRES_DB_HOST")
    port = get_env_value("POSTGRES_DB_PORT")
    name = get_env_value("POSTGRES_DB_NAME")
    user = get_env_value("POSTGRES_DB_USER")
    password = get_env_value("POSTGRES_DB_PASSWORD")
    if "test" in sys.argv:
        DATABASES[tenant] = {
            "ENGINE": db_engine_postgres,
            "HOST": host,
            "PORT": port,
            "NAME": name,
            "USER": user,
            "PASSWORD": password,
            "OPTIONS": {
                "options": "-c search_path=public",
                "sslmode": "require",
            },
        }
    else:
        DATABASES[tenant] = {
            "ENGINE": db_engine_postgres,
            "HOST": host,
            "PORT": port,
            "NAME": name,
            "USER": user,
            "PASSWORD": password,
            "OPTIONS": {
                "options": f"-c search_path={get_env_value(f'DB_SCHEMA_{tenant}')}",
                "sslmode": "require",
            },
        }


def add_database_config_for_oracle(tenant):
    import oracledb

    oracledb.version = "8.3.0"
    sys.modules["cx_Oracle"] = oracledb
    DATABASES[tenant] = {
        "ENGINE": "django.db.backends.oracle",
        "HOST": get_env_value(f"ORACLE_DB_HOST_{tenant}"),
        "PORT": get_env_value(f"ORACLE_DB_PORT_{tenant}"),
        "NAME": get_env_value(f"ORACLE_DB_NAME_{tenant}"),
        "USER": os.getenv(f"DB_SCHEMA_{tenant}", os.getenv(f"ORACLE_DB_USER_{tenant}")),
        "PASSWORD": get_env_value(f"ORACLE_DB_PASSWORD_{tenant}"),
        "OPTIONS": {"threaded": True},
    }


def add_database_config_for_oracle_easy_connect(tenant):
    DATABASES[tenant] = {
        "ENGINE": db_engine_oracle,
        "NAME": get_env_value("DB_NAME"),
        "USER": get_env_value("DB_USER"),
        "PASSWORD": get_env_value("DB_PASSWORD"),
        "OPTIONS": {"threaded": True},
    }


def add_database_config_for_oracle_full_connect(tenant):
    protocol = get_env_value("DB_PROTOCOL")
    port = get_env_value("DB_PORT")
    host = get_env_value("DB_HOST")
    service_name = get_env_value("DB_SERVICE_NAME")

    DATABASES[tenant] = {
        "NAME": (
            f"(DESCRIPTION=(ADDRESS=(PROTOCOL={protocol})(HOST={host})(PORT={port}))"
            f"(CONNECT_DATA=(SERVICE_NAME={service_name})))"
        ),
        "ENGINE": db_engine_oracle,
        "USER": get_env_value("DB_USER"),
        "PASSWORD": get_env_value("DB_PASSWORD"),
        "OPTIONS": {"threaded": True},
    }


TENANTS = get_array_like_env("TENANTS")

engine_to_engine = {
    "oracle_easy_connect": add_database_config_for_oracle_easy_connect,
    "oracle_full_connect": add_database_config_for_oracle_full_connect,
    "oracle": add_database_config_for_oracle,
    "postgres_schema": add_database_config_for_postgres_schema,
    "postgres_schema_ssl": add_database_config_for_postgres_schema_with_ssl,
    "sqlite": add_database_config_for_sqlite,
}

for connection in TENANTS:
    engine = get_env_value("DB_ENGINE_default")
    engine_to_engine[engine](connection)

# Database Router For Multi tenant applications

DATABASE_ROUTERS = ["boilerplate.lib.utils.db_router.DatabaseRouter"]

# Logger Configuration

LOGLEVEL = get_env_value("LOGLEVEL").upper()

django_server = "django.server"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {},
    "formatters": {
        "logfile": {
            # exact format is not important, this is the minimum information
            "format": "%(asctime)s %(name)-25s %(levelname)-8s %(message)s",
        },
        django_server: DEFAULT_LOGGING["formatters"][django_server],
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "logfile",
            "filters": [],
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "logfile",
            "filename": f"{os.path.join(BASE_DIR, 'analytics.log')}",
            "when": "W0",  # daily, you can use 'midnight' as well
            "backupCount": 100,  # 100 days backup
        },
        # Add Handler for Sentry for `warning` and above
        # 'sentry': {
        #     'level': 'WARNING',
        #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        # },
        django_server: DEFAULT_LOGGING["handlers"][django_server],
    },
    "loggers": {
        # root logger
        "": {"level": "WARNING", "handlers": ["console", "file"]},  # , 'sentry'],
        "celery": {
            "level": LOGLEVEL,
            "handlers": ["file", "console"],  # , 'sentry'],
            # required to avoid double logging with root logger
            "propagate": False,
        },
        "main": {
            "level": LOGLEVEL,
            "handlers": ["console", "file"],  # , 'sentry'],
            # required to avoid double logging with root logger
            "propagate": False,
        },
        "db_router": {
            "level": LOGLEVEL,
            "handlers": ["console", "file"],  # , 'sentry'],
            # required to avoid double logging with root logger
            "propagate": False,
        },
        "metadata": {
            "level": LOGLEVEL,
            "handlers": ["console", "file"],  # , 'sentry'],
            # required to avoid double logging with root logger
            "propagate": False,
        },
        "django_celery_beat": {
            "level": LOGLEVEL,
            "handlers": ["console", "file"],  # , 'sentry'],
            # required to avoid double logging with root logger
            "propagate": False,
        },
        # Don't send this module's logs to Sentry
        "noise": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "reports": {
            "level": LOGLEVEL,
            "handlers": ["console", "file"],  # , 'sentry'],
            # required to avoid double logging with root logger
            "propagate": False,
        },
        django_server: DEFAULT_LOGGING["loggers"][django_server],
        "django.request": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.api": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# Cross Origin
CORS_ORIGIN_ALLOW_ALL = get_boolean_env_value("CORS_ORIGIN_ALLOW_ALL")

if USE_REDIS := get_boolean_env_value("USE_REDIS"):
    REDIS_HOST = get_env_value("REDIS_HOST")
    REDIS_PASSWORD = get_env_value("REDIS_PASSWORD")
    REDIS_TIMEOUT = get_env_value("REDIS_TIMEOUT")
    REDIS_PORT = get_env_value("REDIS_PORT")

if USE_CELERY := get_boolean_env_value("USE_CELERY"):
    CELERY_BROKER_URL = get_env_value("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = get_env_value("CELERY_RESULT_BACKEND")
    CELERY_CACHE_BACKEND = get_env_value("CELERY_CACHE_BACKEND")

if USE_EVENT_LOGGER := get_boolean_env_value("USE_EVENT_LOGGER"):
    KOMBU_BROKER_URL = get_env_value("KOMBU_BROKER_URL")

if USE_CACHE := get_boolean_env_value("USE_CACHE"):
    CACHE_BACKEND = get_env_value("CACHE_BACKEND")
    CACHE_LOCATION = get_env_value("CACHE_LOCATION")
    CACHE_TIMEOUT = get_env_value("CACHE_TIMEOUT")
    CACHES = {
        "default": {
            "BACKEND": CACHE_BACKEND,
            "LOCATION": CACHE_LOCATION,
            "TIMEOUT": CACHE_TIMEOUT,
        }
    }

# Minio Configurations
USE_MINIO_INTERNAL_CLIENT = get_boolean_env_value("USE_MINIO_INTERNAL_CLIENT")
USE_MINIO_EXTERNAL_CLIENT = get_boolean_env_value("USE_MINIO_INTERNAL_CLIENT")
MINIO_BUCKET_NAME = get_env_value("MINIO_BUCKET_NAME")
if USE_MINIO_INTERNAL_CLIENT:
    MINIO_URL_INTERNAL = get_env_value("MINIO_URL_INTERNAL")
    MINIO_ACCESS_KEY = get_env_value("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = get_env_value("MINIO_SECRET_KEY")
    MINIO_LINK_EXPIRY_TIMEOUT = int(get_env_value("MINIO_LINK_EXPIRY_TIMEOUT"))
    BOTO_CLIENT_PUSH = boto3.client(
        "s3",
        endpoint_url=MINIO_URL_INTERNAL,
        config=boto3.session.Config(signature_version="s3v4"),
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )
    if USE_MINIO_EXTERNAL_CLIENT:
        MINIO_URL_EXTERNAL = get_env_value("MINIO_URL_EXTERNAL")
        BOTO_CLIENT_RETRIEVE = boto3.client(
            "s3",
            endpoint_url=MINIO_URL_EXTERNAL,
            config=boto3.session.Config(signature_version="s3v4"),
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
        )

# APIClient Settings
DEFAULT_REQUEST_TIMEOUT = get_env_value("DEFAULT_REQUEST_TIMEOUT")
USE_DATABASE_AS_DEFAULT = get_boolean_env_value("USE_DATABASE_AS_DEFAULT")

DEFAULT_LOCALE = get_env_value("DEFAULT_LOCALE")
SUPPORTED_LOCALES = get_array_like_env("SUPPORTED_LOCALES")


def load_error_messages(file_path):
    error_messages = {}
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for locale in SUPPORTED_LOCALES:
                error_messages[f"{row['code']}_{locale}"] = row[f"detail_{locale}"]

    return error_messages


ERROR_MESSAGES = load_error_messages(file_path="error-messages.csv")

DRF_STANDARDIZED_ERRORS = {
    "EXCEPTION_HANDLER_CLASS": "lib.exception_handling.StandardExceptionHandler",
    "EXCEPTION_FORMATTER_CLASS": "lib.exception_handling.StandardExceptionFormatter",
}

USE_METADATA = get_boolean_env_value("USE_METADATA")

MAX_PDF_LIMIT = get_int_env_value("MAX_PDF_LIMIT")

# logger envs
LOGLEVEL = get_env_value("LOGLEVEL").upper()
LOG_INTO_FILE = get_boolean_env_value("LOG_INTO_FILE")
LOG_WITH_COLOR_IN_CONSOLE = get_boolean_env_value("LOG_WITH_COLOR_IN_CONSOLE")

if LOG_INTO_FILE:
    LOG_WITH_COLOR_IN_FILE = get_boolean_env_value("LOG_WITH_COLOR_IN_FILE")
    LOG_BACKUP = get_int_env_value("LOG_BACKUP")  # no of days
    LOG_WHEN = get_env_value("LOG_WHEN")
    LOG_FILE_NAME = get_env_value("LOG_FILE_NAME")
    LOGGING = get_logger_config_with_file(
        base_dir=BASE_DIR,
        log_level=LOGLEVEL,
        log_backup=LOG_BACKUP,
        log_when=LOG_WHEN,
        log_file_name=LOG_FILE_NAME,
        log_color_console=LOG_WITH_COLOR_IN_CONSOLE,
        log_color_file=LOG_WITH_COLOR_IN_FILE,
    )
else:
    LOGGING = get_logger_config_without_file(
        log_level=LOGLEVEL, log_color=LOG_WITH_COLOR_IN_CONSOLE
    )

SERVICE_NAME = get_env_value("SERVICE_NAME")
LOG_ACTIVITY_PUBSUB = get_boolean_env_value("LOG_ACTIVITY_PUBSUB")
PUBSUB = NatsPubSub() if os.getenv("PUBSUB_BROKEN") == "nats" else KombuPubSub()

PAYMENT_CATEGORY_QR = get_env_value("PAYMENT_CATEGORY_QR")

USE_OFFSET = get_boolean_env_value("USE_OFFSET")

ENABLE_BRANCH_FILTER = get_boolean_env_value("ENABLE_BRANCH_FILTER")

EXCHANGES = [
    {"NAME": "analytics_publish", "TYPE": "direct", "DURABLE": True},
    {"NAME": "analytics_schedule", "TYPE": "direct", "DURABLE": True},
    {"NAME": "scheduler_email", "TYPE": "direct", "DURABLE": True},
    {"NAME": "analytics_events", "TYPE": "direct", "DURABLE": True},
    {"NAME": "campaign_data", "TYPE": "direct", "DURABLE": True},
]

PIKA_SETTINGS = {
    "BROKER_URL": get_env_value("ANALYTICS_BROKER_URL"),
    "ENABLE_PUBLISHER_CONFIRMS": get_boolean_env_value("ENABLE_PUBLISHER_CONFIRMS"),
}

PICSUM_URL = get_env_value("PICSUM_URL")

TIME_SKIP_VIEWS = get_int_env_value("TIME_SKIP_VIEWS")

logging.getLogger("pika").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)

DNS = get_env_value("DNS")
GIT_TOKEN = get_env_value("GIT_TOKEN")

INTERNAL_PERMISSIONS_API = get_env_value("INTERNAL_PERMISSIONS_API")
STUB_INTERNAL_PERMISSIONS_API = get_boolean_env_value("STUB_INTERNAL_PERMISSIONS_API")
EVENTLOGGER_SCHEDULE_UPDATE = get_env_value("EVENTLOGGER_SCHEDULE_UPDATE")
GIT_WORKSPACE = get_env_value("GIT_WORKSPACE")
GIT_HTTP_PROXY_URL = get_env_value("GIT_HTTP_PROXY_URL")
GIT_USER = get_env_value("GIT_USER")
GIT_PROVIDER = get_env_value("GIT_PROVIDER")
