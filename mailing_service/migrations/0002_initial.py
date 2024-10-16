# Generated by Django 5.1.1 on 2024-10-11 12:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("mailing_service", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="clients",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="clients",
            field=models.ManyToManyField(
                to="mailing_service.client", verbose_name="Клиенты"
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mailings",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
        migrations.AddField(
            model_name="mailingattempt",
            name="mailing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="mailing_service.mailing",
                verbose_name="Рассылка",
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="message",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="mailing_service.message",
                verbose_name="Сообщение",
            ),
        ),
    ]
