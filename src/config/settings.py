import os
import secrets

from split_settings.tools import include

SECRET_KEY = str(os.environ.get("SECRET_KEY") or secrets.token_hex(32))

DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t", "yes", "y")
USE_SQLITE = os.environ.get("USE_SQLITE", "False").lower() in (
    "true",
    "1",
    "t",
    "yes",
    "y",
)

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
ADMIN_URL = os.environ.get("ADMIN_URL", None)
APP_NAME = os.environ.get("APP_NAME")

config_folder = "components/"

config_files = [
    "api.py",
    "apps.py",
    "auth.py",
    "boilerplate.py",
    "database.py",
    "templates.py",
    "internationalization.py",
    "logging.py",
    "static.py",
    "middleware.py",
    "timezone.py",
]

include(*(config_folder + file for file in config_files))
