from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="manager@test.com",
            first_name="I am",
            last_name="MANAGER",
        )

        user.set_password("12345678")

        group, created = Group.objects.get_or_create(name="manager")
        user.groups.add(group)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(f"Менеджер manager@test.com успешно создан")
        )

        user = User.objects.create(
            email="content_manager@test.com",
            first_name="I am",
            last_name="CONTENT MANAGER",
            is_staff=True,
        )

        user.set_password("12345678")

        group, created = Group.objects.get_or_create(name="content_manager")
        user.groups.add(group)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Контент-менеджер content_manager@test.com успешно создан"
            )
        )
