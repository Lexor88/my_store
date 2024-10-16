# Generated by Django 5.1.1 on 2024-10-11 12:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BlogPost",
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
                ("title", models.CharField(max_length=200, verbose_name="Заголовок")),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        max_length=200,
                        unique=True,
                        verbose_name="URL-адрес",
                    ),
                ),
                ("content", models.TextField(verbose_name="Содержание")),
                (
                    "preview_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="blog_previews/",
                        verbose_name="Изображение превью",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(default=False, verbose_name="Опубликован"),
                ),
                (
                    "views",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Количество просмотров"
                    ),
                ),
            ],
            options={
                "permissions": [("can_manage_blog", "Can manage blog posts")],
            },
        ),
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
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=200, verbose_name="Название")),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        max_length=200,
                        unique=True,
                        verbose_name="URL-адрес",
                    ),
                ),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Цена"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="product_images/",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        default="Uncategorized",
                        max_length=100,
                        verbose_name="Категория",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата изменения"),
                ),
                (
                    "is_published",
                    models.BooleanField(default=False, verbose_name="Опубликован"),
                ),
            ],
            options={
                "permissions": [
                    ("can_publish_product", "Can publish/unpublish product"),
                    ("can_change_description", "Can change product description"),
                    ("can_change_category", "Can change product category"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Version",
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
                    "version_name",
                    models.CharField(max_length=100, verbose_name="Название версии"),
                ),
                (
                    "version_number",
                    models.CharField(max_length=10, verbose_name="Номер версии"),
                ),
                (
                    "is_current_version",
                    models.BooleanField(default=False, verbose_name="Текущая версия"),
                ),
            ],
        ),
    ]
