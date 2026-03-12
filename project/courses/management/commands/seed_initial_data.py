from pathlib import Path

from django.core.management import BaseCommand, call_command
from django.db import connection

from blog.models import Category, Post
from courses.models import Course


class Command(BaseCommand):
    help = "Load initial project data only when the database is empty."

    def handle(self, *args, **options):
        self.stdout.write(
            f"Seeding check on database engine={connection.vendor} name={connection.settings_dict.get('NAME')}"
        )

        has_existing_data = any(
            [
                Category.objects.exists(),
                Post.objects.exists(),
                Course.objects.exists(),
            ]
        )

        if has_existing_data:
            self.stdout.write(self.style.WARNING("Initial data already exists. Skipping."))
            return

        fixture_path = Path(__file__).resolve().parents[3] / "content_seed.json"
        self.stdout.write(f"Using fixture: {fixture_path}")

        if not fixture_path.exists():
            raise FileNotFoundError(
                f"Fixture file not found: {fixture_path}"
            )

        call_command("loaddata", str(fixture_path))

        counts = {
            "categories": Category.objects.count(),
            "posts": Post.objects.count(),
            "courses": Course.objects.count(),
        }
        self.stdout.write(f"Post-seed counts: {counts}")

        if not any(counts.values()):
            raise RuntimeError("Seeding completed without inserting any records.")

        self.stdout.write(self.style.SUCCESS("Initial data loaded successfully."))
