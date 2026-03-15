from django.conf import settings
from django.db import migrations


def set_admin3_password(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)

    try:
        user = User.objects.get(username="admin3")
    except User.DoesNotExist:
        return

    user.password = "pbkdf2_sha256$1200000$21B3EOKwaTsL97K6NpeZsh$wPT/YE2qc1BQotBd15zU4AGp/toy7/CqHVDyfBmUzHE="
    user.save(update_fields=["password"])


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(set_admin3_password, migrations.RunPython.noop),
    ]
