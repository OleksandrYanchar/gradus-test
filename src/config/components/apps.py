from django.conf import settings

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY = [
    "rest_framework",
    "drf_yasg",
]

LOCAL_APPS = [
    "users",
    "health",
]

DEBUG_APPS = []

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY + LOCAL_APPS

if settings.DEBUG:
    INSTALLED_APPS += DEBUG_APPS
