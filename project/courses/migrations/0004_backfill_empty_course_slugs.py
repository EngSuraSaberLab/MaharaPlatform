from django.db import migrations
from django.utils.text import slugify


def backfill_empty_course_slugs(apps, schema_editor):
    Course = apps.get_model("courses", "Course")

    for course in Course.objects.filter(slug="").order_by("pk"):
        base_slug = slugify(course.title, allow_unicode=True) or f"course-{course.pk}"
        slug = base_slug
        counter = 1

        while Course.objects.filter(slug=slug).exclude(pk=course.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        course.slug = slug
        course.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0003_alter_course_slug"),
    ]

    operations = [
        migrations.RunPython(backfill_empty_course_slugs, migrations.RunPython.noop),
    ]
