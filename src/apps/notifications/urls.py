from django.urls import include, path

urlpatterns = [
    path("", include("notifications.api.urls")),
]
