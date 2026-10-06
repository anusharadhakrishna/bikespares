from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = "Create Django superuser if it does not already exist"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.getenv("ADMIN_USERNAME", "admin")
        email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        password = os.getenv("ADMIN_PASSWORD")

        if not password:
            self.stdout.write(
                self.style.WARNING(
                    "ADMIN_PASSWORD is not set. Skipping superuser creation."
                )
            )
            return

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Superuser '{username}' already exists."
                )
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Superuser '{username}' created successfully."
            )
        )