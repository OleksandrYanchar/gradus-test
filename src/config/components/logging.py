import os
from datetime import datetime

from django.conf import settings

from config.components.boilerplate import BASE_DIR

LOGGING_DIR = os.path.join(BASE_DIR.parent, "logs")

if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

if settings.DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(
                    LOGGING_DIR,
                    f"{datetime.now():%Y-%m-%d}_log",
                ),
                "when": "midnight",
                "backupCount": 7,
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "django.db.backends": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
    }
else:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
            "file": {
                "level": "ERROR",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(
                    LOGGING_DIR,
                    f"{datetime.now():%Y-%m-%d}_log",
                ),
                "when": "midnight",
                "backupCount": 7,
                "encoding": "utf-8",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "ERROR",
        },
    }
