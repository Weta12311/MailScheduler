from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@test.com",
            first_name="I am",
            last_name="SUPERUSER",
            is_staff=True,
            is_superuser=True,
        )

        user.set_password("12345678")
        user.save()

        self.stdout.write(
            self.style.SUCCESS(f"Суперпользователь admin@test.com успешно создан")
        )
