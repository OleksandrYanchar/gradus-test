from django.core.exceptions import ValidationError
from django.db import models


class NotificationChannel(models.TextChoices):
    EMAIL = "email", "Email"
    TELEGRAM = "telegram", "Telegram"
    VIBER = "viber", "Viber"
    PUSH = "push", "Push"


class NotificationType(models.Model):
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=255)
    allowed_channels = models.JSONField(default=list, blank=True)
    allowed_variables = models.JSONField(default=list, blank=True)
    is_singleton_template = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Notification Type"
        verbose_name_plural = "Notification Types"

    def __str__(self) -> str:
        return f"{self.code}"


class NotificationTemplate(models.Model):
    type = models.ForeignKey(
        NotificationType,
        on_delete=models.PROTECT,
        related_name="templates",
    )
    name = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    html = models.TextField()

    class Meta:
        verbose_name = "Notification Template"
        verbose_name_plural = "Notification Templates"
        constraints = [
            models.UniqueConstraint(
                fields=["type", "name"],
                name="notifications_template_type_name_unique",
            ),
        ]

    def __str__(self) -> str:
        label = self.name or self.type.code
        return f"{self.type.code}:{label}"

    def clean(self):
        super().clean()

        if self.type is None:
            return

        if self.type.is_singleton_template:
            exists = NotificationTemplate.objects.filter(type=self.type).exclude(pk=self.pk).exists()
            if exists:
                raise ValidationError(
                    {"type": "Template for this notification type already exists."},
                )

        if self.type.code == "custom":
            if not self.name:
                raise ValidationError({"name": "Name is required for custom templates."})
        else:
            if self.name:
                raise ValidationError({"name": "Name is only allowed for custom templates."})
