from dataclasses import dataclass

from django.template import Context, Template
from notifications.models import (
    NotificationChannel,
    NotificationTemplate,
    NotificationType,
)
from notifications.services.channels import BaseChannel, EmailChannel


@dataclass
class RenderedTemplate:
    title: str
    html: str


class NotificationService:
    def __init__(self, channels: list[BaseChannel] | None = None) -> None:
        self._channels = {channel.channel: channel for channel in (channels or [EmailChannel()])}

    def send_new_survey(self, user, title: str, channels: list[str] | None = None) -> None:
        self._send_by_type(
            user=user,
            type_code="new_survey",
            context={"title": title},
            channels=channels,
        )

    def send_confirm_email(self, user, confirmation_token: str, channels: list[str] | None = None) -> None:
        self._send_by_type(
            user=user,
            type_code="confirm_email",
            context={"confirmation_token": confirmation_token},
            channels=channels,
        )

    def send_bot_successful_subscribe(self, user, username: str, channels: list[str] | None = None) -> None:
        self._send_by_type(
            user=user,
            type_code="bot_successful_subscribe",
            context={"username": username},
            channels=channels,
        )

    def send_custom(
        self,
        user,
        name: str,
        channels: list[str] | None = None,
        context: dict | None = None,
    ) -> None:
        self._send_by_type(
            user=user,
            type_code="custom",
            template_name=name,
            context=context or {},
            channels=channels,
        )

    def _send_by_type(
        self,
        user,
        type_code: str,
        context: dict,
        channels: list[str] | None,
        template_name: str | None = None,
    ) -> None:
        notification_type = NotificationType.objects.get(code=type_code)
        template = self._get_template(notification_type, template_name)

        self._validate_context(notification_type, context)

        resolved_channels = channels or notification_type.allowed_channels
        self._validate_channels(notification_type, resolved_channels)

        rendered = self._render_template(template, context)

        for channel in resolved_channels:
            self._send_to_channel(user, channel, rendered)

    @staticmethod
    def _get_template(notification_type: NotificationType, name: str | None) -> NotificationTemplate:
        if notification_type.code == "custom":
            if not name:
                raise ValueError("Custom template name is required.")
            return NotificationTemplate.objects.get(type=notification_type, name=name)

        return NotificationTemplate.objects.get(type=notification_type)

    @staticmethod
    def _validate_context(notification_type: NotificationType, context: dict) -> None:
        required = set(notification_type.allowed_variables or [])
        missing = required - set(context.keys())
        if missing:
            raise ValueError(f"Missing context variables: {sorted(missing)}.")

    @staticmethod
    def _validate_channels(notification_type: NotificationType, channels: list[str]) -> None:
        allowed = set(notification_type.allowed_channels or [])
        invalid = set(channels) - allowed
        if invalid:
            raise ValueError(f"Channels not allowed for type {notification_type.code}: {sorted(invalid)}.")

    @staticmethod
    def _render_template(template: NotificationTemplate, context: dict) -> RenderedTemplate:
        return RenderedTemplate(
            title=Template(template.title or "").render(Context(context)),
            html=Template(template.html).render(Context(context)),
        )

    def _send_to_channel(self, user, channel: str, rendered: RenderedTemplate) -> None:
        if channel not in self._channels:
            raise NotImplementedError(f"Channel not implemented: {channel}.")

        if channel == NotificationChannel.EMAIL:
            recipient = getattr(user, "email", None)
        else:
            recipient = None

        self._channels[channel].send(recipient, rendered.title, rendered.html)
