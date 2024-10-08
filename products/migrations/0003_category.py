# Generated by Django 5.1.1 on 2024-10-03 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_blogpost_alter_product_options_product_category_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Название категории"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        max_length=100,
                        unique=True,
                        verbose_name="URL-адрес категории",
                    ),
                ),
            ],
        ),
    ]
