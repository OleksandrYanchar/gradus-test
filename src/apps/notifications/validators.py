import re

import bleach
from django.template import Template, TemplateSyntaxError
from notifications.models import NotificationChannel

EMAIL_ALLOWED_TAGS = ["p", "b", "i", "a", "br"]
BOT_ALLOWED_TAGS = ["p", "br"]

PUSH_TAG_PATTERN = re.compile(r"<[^>]+>")
IF_TAG_PATTERN = re.compile(r"{%\s*if\s+([a-zA-Z_][\w\.]*)\s*%}")
VAR_TAG_PATTERN = re.compile(r"{{\s*([a-zA-Z_][\w\.]*)\s*}}")


class TemplateValidationError(ValueError):
    pass


def validate_template_syntax(html: str) -> None:
    try:
        Template(html)
    except TemplateSyntaxError as exc:
        raise TemplateValidationError(f"Invalid django template: {exc}") from exc


def _validate_html_tags_for_channel(html: str, channel: str) -> None:
    if channel == NotificationChannel.PUSH:
        if PUSH_TAG_PATTERN.search(html):
            raise TemplateValidationError("Push templates cannot contain HTML tags.")
        return

    allowed_tags = EMAIL_ALLOWED_TAGS if channel == NotificationChannel.EMAIL else BOT_ALLOWED_TAGS
    cleaned = bleach.clean(
        html,
        tags=allowed_tags,
        attributes={"a": ["href", "title", "target"]},
        strip=True,
    )
    if cleaned != html:
        raise TemplateValidationError(
            f"Template contains forbidden HTML tags for channel: {channel}.",
        )


def validate_html_for_channels(html: str, allowed_channels: list[str]) -> None:
    for channel in allowed_channels:
        _validate_html_tags_for_channel(html, channel)


def validate_title_for_channels(title: str, allowed_channels: list[str]) -> None:
    if NotificationChannel.TELEGRAM in allowed_channels or NotificationChannel.VIBER in allowed_channels:
        if title:
            raise TemplateValidationError("Title must be empty for telegram/viber channels.")


def extract_template_variables(html: str) -> set[str]:
    vars_from_tags = {match.group(1) for match in VAR_TAG_PATTERN.finditer(html)}
    vars_from_if = {match.group(1) for match in IF_TAG_PATTERN.finditer(html)}
    return vars_from_tags | vars_from_if


def validate_template_variables(html: str, allowed_variables: list[str]) -> None:
    present = extract_template_variables(html)
    allowed_set = set(allowed_variables or [])

    missing = allowed_set - present
    extra = present - allowed_set

    if missing:
        raise TemplateValidationError(f"Missing variables in template: {sorted(missing)}.")
    if extra:
        raise TemplateValidationError(f"Template contains unsupported variables: {sorted(extra)}.")
