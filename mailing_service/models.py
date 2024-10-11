from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    name = models.CharField(max_length=100, verbose_name="Имя")
    full_name = models.CharField(max_length=255, verbose_name="Полное имя")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clients",
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.email


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема")
    body = models.TextField(verbose_name="Текст сообщения")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = [
        ("created", "Создана"),
        ("running", "Запущена"),
        ("completed", "Завершена"),
    ]
    start_date = models.DateTimeField(default=timezone.now, verbose_name="Дата начала")
    periodicity = models.CharField(
        max_length=10,
        choices=[("day", "Ежедневно"), ("week", "Еженедельно")],
        default="day",
        verbose_name="Периодичность",
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="created", verbose_name="Статус"
    )
    message = models.OneToOneField(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Владелец",
    )

    def clean(self):
        # Проверка на то, что дата начала рассылки в будущем
        if self.start_date <= timezone.now():
            raise ValidationError("Дата начала рассылки должна быть в будущем.")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"{self.message.subject} - {self.get_status_display()}"


class MailingAttempt(models.Model):
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время попытки")
    status = models.CharField(
        max_length=10,
        choices=[("success", "Успешно"), ("failure", "Неуспешно")],
        verbose_name="Статус",
    )
    response = models.TextField(verbose_name="Ответ")

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"

    def __str__(self):
        return f"Attempt for {self.mailing} at {self.timestamp} - Status: {self.status}"
