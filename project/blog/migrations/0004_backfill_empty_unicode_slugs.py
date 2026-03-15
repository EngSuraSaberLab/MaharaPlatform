from django.db import migrations
from django.utils.text import slugify


def build_unique_slug(model, instance, source_value, fallback_prefix):
    base_slug = slugify(source_value, allow_unicode=True) or f"{fallback_prefix}-{instance.pk}"
    slug = base_slug
    counter = 1

    while model.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


def backfill_empty_blog_slugs(apps, schema_editor):
    Category = apps.get_model("blog", "Category")
    Post = apps.get_model("blog", "Post")

    for category in Category.objects.filter(slug="").order_by("pk"):
        category.slug = build_unique_slug(Category, category, category.name, "category")
        category.save(update_fields=["slug"])

    for post in Post.objects.filter(slug="").order_by("pk"):
        post.slug = build_unique_slug(Post, post, post.title, "post")
        post.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_alter_category_slug_alter_post_slug"),
    ]

    operations = [
        migrations.RunPython(backfill_empty_blog_slugs, migrations.RunPython.noop),
    ]
