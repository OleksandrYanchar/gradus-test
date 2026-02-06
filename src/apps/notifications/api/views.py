from notifications.api.serializers import (
    NotificationSendSerializer,
    NotificationTemplateSerializer,
    NotificationTypeSerializer,
)
from notifications.models import NotificationTemplate, NotificationType
from notifications.services.senders import NotificationService
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User

from core.permissions import IsSuperUser


class NotificationTypeViewSet(viewsets.ModelViewSet):
    queryset = NotificationType.objects.all()
    serializer_class = NotificationTypeSerializer
    permission_classes = [IsSuperUser]
    http_method_names = ["get", "post", "head", "options"]


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.select_related("type").all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsSuperUser]
    http_method_names = ["get", "post", "patch", "put", "delete", "head", "options"]

    def perform_destroy(self, instance):
        if instance.type.code != "custom":
            raise ValidationError("Only custom templates can be deleted.")
        return super().perform_destroy(instance)


class NotificationSendAPIView(APIView):
    permission_classes = [IsSuperUser]

    def post(self, request, *args, **kwargs):
        serializer = NotificationSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = User.objects.get(pk=data["user_id"])
        except User.DoesNotExist as exc:
            raise ValidationError({"user_id": "User not found."}) from exc

        service = NotificationService()
        type_code = data["type_code"]
        channels = data.get("channels")
        context = data.get("context") or {}

        try:
            if type_code == "new_survey":
                service.send_new_survey(user, title=context.get("title"), channels=channels)
            elif type_code == "confirm_email":
                service.send_confirm_email(
                    user,
                    confirmation_token=context.get("confirmation_token"),
                    channels=channels,
                )
            elif type_code == "bot_successful_subscribe":
                service.send_bot_successful_subscribe(
                    user,
                    username=context.get("username"),
                    channels=channels,
                )
            elif type_code == "custom":
                service.send_custom(
                    user,
                    name=data["template_name"],
                    channels=channels,
                    context=context,
                )
            else:
                raise ValidationError({"type_code": "Unsupported notification type."})
        except (ValueError, NotificationTemplate.DoesNotExist, NotificationType.DoesNotExist) as exc:
            raise ValidationError(str(exc)) from exc
        except NotImplementedError as exc:
            raise ValidationError(str(exc)) from exc

        return Response({"status": "sent"}, status=status.HTTP_200_OK)
