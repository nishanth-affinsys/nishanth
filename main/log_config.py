import os
from django.utils.log import DEFAULT_LOGGING


def get_logger_config_with_file(
    base_dir,
    log_level,
    log_file_name,
    log_color_console,
    log_color_file,
    log_backup=100,
    log_when="W0",
):
    if log_color_console:
        log_formatter_console = "log_with_color"
    else:
        log_formatter_console = "log_no_color"

    if log_color_file:
        log_formatter_file = "log_with_color"
    else:
        log_formatter_file = "log_no_color"

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {},
        "formatters": {
            "log_with_color": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s[%(asctime)s] [%(process)s : %(thread)s] [%(levelname)s] [%(name)25s:%(lineno)d  %(funcName)s()] %(message)s",
                "log_colors": {
                    "DEBUG": "blue",
                    "INFO": "bold_white",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            },
            "log_no_color": {
                "format": "[%(asctime)s] [%(process)s : %(thread)s] [%(levelname)s] [%(name)25s:%(lineno)d  %(funcName)s() ] %(message)s",
            },
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": log_formatter_console,
                "filters": [],
            },
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": log_formatter_file,
                "filename": f"{os.path.join(base_dir, f'logs/{log_file_name}')}",
                "when": log_when,  # daily, you can use 'midnight' as well
                "backupCount": log_backup,  # 100 days backup
            },
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            # root logger
            "": {"level": "WARNING", "handlers": ["console", "file"]},
            "celery": {
                "level": log_level,
                "handlers": ["file", "console"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "main": {
                "level": log_level,
                "handlers": ["console", "file"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "django_celery_beat": {
                "level": log_level,
                "handlers": ["console", "file"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "console": {
                "level": log_level,
                "handlers": ["console", "file"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "handoff": {
                "level": log_level,
                "handlers": ["console", "file"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "onboarding": {
                "level": log_level,
                "handlers": ["console", "file"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "campaign_manager": {
                "level": log_level,
                "handlers": ["console", "file"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "clickstream": {
                "level": log_level,
                "handlers": ["console", "file"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "client_specific": {
                "level": log_level,
                "handlers": ["console", "file"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "complaints": {
                "level": log_level,
                "handlers": ["console", "file"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "django.server": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False,
            },
            "django.request": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False,
            },
        },
    }
    return LOGGING


def get_logger_config_without_file(log_level, log_color):
    if log_color:
        log_formatter = "log_with_color"
    else:
        log_formatter = "log_no_color"
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {},
        "formatters": {
            "log_with_color": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s[%(asctime)s] [%(process)s : %(thread)s] [%(levelname)s] [%(name)25s:%(lineno)d  %(funcName)s()] %(message)s",
                "log_colors": {
                    "DEBUG": "blue",
                    "INFO": "bold_white",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            },
            "log_no_color": {
                # exact format is not important, this is the minimum information
                "format": "[%(asctime)s] [%(process)s : %(thread)s] [%(levelname)s] [%(name)25s:%(lineno)d  %(funcName)s() ] %(message)s",
            },
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": log_formatter,
                "filters": [],
            },
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            # root logger
            "": {"level": log_level, "handlers": ["console"]},
            "celery": {
                "level": log_level,
                "handlers": ["console"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "main": {
                "level": log_level,
                "handlers": ["console"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "django_celery_beat": {
                "level": log_level,
                "handlers": ["console"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "Your-App-Name": {
                "level": log_level,
                "handlers": ["console"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "django.server": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
            "django.request": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
        },
    }
    return LOGGING
