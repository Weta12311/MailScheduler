from django.contrib import admin

from mailing.models import Mailing, Message, Client, MailingAttempt


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "is_active",
        "send_time",
        "frequency",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "email", "full_name")


@admin.register(MailingAttempt)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id",)
