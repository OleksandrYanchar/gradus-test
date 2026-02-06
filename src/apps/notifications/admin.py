from django.contrib import admin
from notifications.models import NotificationTemplate, NotificationType


@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_singleton_template")
    search_fields = ("code", "name")


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ("type", "name", "title")
    search_fields = ("name", "title")
    list_filter = ("type",)
