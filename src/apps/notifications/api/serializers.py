from django.core.exceptions import ValidationError as DjangoValidationError
from notifications.models import (
    NotificationChannel,
    NotificationTemplate,
    NotificationType,
)
from notifications.validators import (
    TemplateValidationError,
    validate_html_for_channels,
    validate_template_syntax,
    validate_template_variables,
    validate_title_for_channels,
)
from rest_framework import serializers


class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = (
            "id",
            "code",
            "name",
            "allowed_channels",
            "allowed_variables",
            "is_singleton_template",
        )

    def validate_allowed_channels(self, value):
        allowed_values = set(NotificationChannel.values)
        invalid = set(value) - allowed_values
        if invalid:
            raise serializers.ValidationError(f"Invalid channels: {sorted(invalid)}.")
        return value

    def validate_allowed_variables(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Allowed variables must be a list.")
        invalid = [item for item in value if not isinstance(item, str) or not item.strip()]
        if invalid:
            raise serializers.ValidationError("Allowed variables must be non-empty strings.")
        return value


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = (
            "id",
            "type",
            "name",
            "title",
            "html",
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        instance = getattr(self, "instance", None)

        notification_type = attrs.get("type") or (instance.type if instance else None)
        if notification_type is None:
            raise serializers.ValidationError({"type": "Notification type is required."})

        html = attrs.get("html") or (instance.html if instance else "")
        title = attrs.get("title") or (instance.title if instance else "")
        allowed_channels = notification_type.allowed_channels or []
        allowed_variables = notification_type.allowed_variables or []

        try:
            validate_template_syntax(html)
            validate_html_for_channels(html, allowed_channels)
            validate_title_for_channels(title, allowed_channels)
            validate_template_variables(html, allowed_variables)

            temp = NotificationTemplate(
                type=notification_type,
                name=attrs.get("name") if "name" in attrs else (instance.name if instance else ""),
                title=title,
                html=html,
            )
            temp.pk = instance.pk if instance else None
            temp.clean()
        except TemplateValidationError as exc:
            raise serializers.ValidationError(str(exc)) from exc
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict or exc.messages) from exc

        return attrs


class NotificationSendSerializer(serializers.Serializer):
    type_code = serializers.SlugField()
    user_id = serializers.IntegerField()
    template_name = serializers.CharField(required=False, allow_blank=False)
    context = serializers.DictField(required=False, default=dict)
    channels = serializers.ListField(
        child=serializers.ChoiceField(choices=NotificationChannel.values),
        required=False,
    )

    def validate(self, attrs):
        attrs = super().validate(attrs)

        try:
            notification_type = NotificationType.objects.get(code=attrs["type_code"])
        except NotificationType.DoesNotExist as exc:
            raise serializers.ValidationError({"type_code": "Unknown notification type."}) from exc

        if notification_type.code == "custom" and not attrs.get("template_name"):
            raise serializers.ValidationError({"template_name": "Template name is required for custom type."})

        return attrs
