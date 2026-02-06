from django.urls import path
from notifications.api.views import (
    NotificationSendAPIView,
    NotificationTemplateViewSet,
    NotificationTypeViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("types", NotificationTypeViewSet, basename="notification-types")
router.register("templates", NotificationTemplateViewSet, basename="notification-templates")

urlpatterns = router.urls
urlpatterns += [
    path("send/", NotificationSendAPIView.as_view(), name="notification-send"),
]
