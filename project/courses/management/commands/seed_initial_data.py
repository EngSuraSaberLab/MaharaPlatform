from pathlib import Path

from django.core.management import BaseCommand, call_command

from blog.models import Category, Post
from courses.models import Course, Enrollment
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Load initial project data only when the database is empty."

    def handle(self, *args, **options):
        has_existing_data = any(
            [
                User.objects.exists(),
                Category.objects.exists(),
                Post.objects.exists(),
                Course.objects.exists(),
                Enrollment.objects.exists(),
            ]
        )

        if has_existing_data:
            self.stdout.write(self.style.WARNING("Initial data already exists. Skipping."))
            return

        fixture_path = Path(__file__).resolve().parents[3] / "initial_data.json"
        if not fixture_path.exists():
            self.stdout.write(
                self.style.WARNING(f"Fixture file not found: {fixture_path}")
            )
            return

        call_command("loaddata", str(fixture_path))
        self.stdout.write(self.style.SUCCESS("Initial data loaded successfully."))
