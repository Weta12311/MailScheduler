from django.apps import AppConfig
import os
import sys


class MailingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing"

    def ready(self):
        if "runserver" in sys.argv and os.environ.get("RUN_MAIN") == "true":
            from mailing.services.scheduler import start_scheduler

            start_scheduler()
