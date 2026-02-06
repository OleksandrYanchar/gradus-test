from django.db import migrations


def add_default_notification_types(apps, schema_editor):
    NotificationType = apps.get_model("notifications", "NotificationType")

    defaults = [
        {
            "code": "new_survey",
            "name": "New survey",
            "allowed_channels": ["email", "telegram", "viber", "push"],
            "allowed_variables": ["title"],
            "is_singleton_template": True,
        },
        {
            "code": "confirm_email",
            "name": "Confirm email",
            "allowed_channels": ["email"],
            "allowed_variables": ["confirmation_token"],
            "is_singleton_template": True,
        },
        {
            "code": "bot_successful_subscribe",
            "name": "Bot successful subscribe",
            "allowed_channels": ["telegram", "viber"],
            "allowed_variables": ["username"],
            "is_singleton_template": True,
        },
        {
            "code": "custom",
            "name": "Custom",
            "allowed_channels": ["email", "telegram", "viber", "push"],
            "allowed_variables": [],
            "is_singleton_template": False,
        },
    ]

    for item in defaults:
        NotificationType.objects.update_or_create(
            code=item["code"],
            defaults=item,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("notifications", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_default_notification_types, migrations.RunPython.noop),
    ]
