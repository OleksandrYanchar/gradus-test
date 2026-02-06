from django.urls import path
from health.api import views

urlpatterns = [
    path("healthcheck/", views.HealthCheckAPIView.as_view(), name="healthcheck"),
]
