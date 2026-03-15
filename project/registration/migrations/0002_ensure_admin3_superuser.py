from django.conf import settings
from django.db import migrations


PASSWORD_HASH = "pbkdf2_sha256$1200000$21B3EOKwaTsL97K6NpeZsh$wPT/YE2qc1BQotBd15zU4AGp/toy7/CqHVDyfBmUzHE="


def ensure_admin3_superuser(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)

    defaults = {
        "password": PASSWORD_HASH,
        "is_staff": True,
        "is_superuser": True,
        "is_active": True,
    }

    user, created = User.objects.get_or_create(
        username="admin3",
        defaults=defaults,
    )

    if created:
        return

    for field, value in defaults.items():
        setattr(user, field, value)
    user.save(update_fields=list(defaults.keys()))


class Migration(migrations.Migration):

    dependencies = [
        ("registration", "0001_set_admin3_password"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(ensure_admin3_superuser, migrations.RunPython.noop),
    ]
