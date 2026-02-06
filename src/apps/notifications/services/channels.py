from abc import ABC, abstractmethod

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from notifications.models import NotificationChannel


class BaseChannel(ABC):
    channel = None

    @abstractmethod
    def send(self, recipient, subject: str, html_body: str) -> None:
        raise NotImplementedError


class EmailChannel(BaseChannel):
    channel = NotificationChannel.EMAIL

    def send(self, recipient, subject: str, html_body: str) -> None:
        if not recipient:
            raise ValueError("Email recipient is required.")

        text_body = strip_tags(html_body or "")
        message = EmailMultiAlternatives(subject=subject, body=text_body, to=[recipient])
        if html_body:
            message.attach_alternative(html_body, "text/html")
        message.send()
