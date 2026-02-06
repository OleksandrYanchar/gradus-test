import os

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from dotenv import load_dotenv
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

load_dotenv()

schema_view = get_schema_view(
    openapi.Info(
        title="AUTH API",
        default_version="v1",
        description="Documentation for helmee API",
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path(os.getenv("ADMIN_URL"), admin.site.urls),
    path("", include("health.urls")),
    path("api/notifications/", include("notifications.urls")),
]

if settings.DEBUG:
    swagger_urlpatterns = [
        path(
            "api/swagger<format>/",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "api/swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "api/redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]

    urlpatterns += swagger_urlpatterns
