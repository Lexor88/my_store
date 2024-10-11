from django.contrib import admin
from .models import Mailing, Message, Client, MailingAttempt
from django.core.exceptions import ObjectDoesNotExist


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ["message", "start_date", "status", "owner"]  # Добавили владельца
    list_filter = ["status", "periodicity"]  # Фильтры по статусу и периодичности
    search_fields = [
        "message__subject",
        "owner__email",
    ]  # Поиск по теме сообщения и email владельца
    ordering = ["-start_date"]  # Сортировка по дате начала (новые сначала)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Managers").exists():
            return qs  # Менеджеры видят все рассылки
        return qs.filter(
            owner=request.user
        )  # Обычные пользователи видят только свои рассылки


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["subject"]
    search_fields = ["subject"]  # Поиск по теме сообщения


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["email", "name"]
    search_fields = ["email", "name"]  # Поиск по email и имени


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ["mailing", "timestamp", "status"]
    list_filter = ["status"]  # Фильтр по статусу
    search_fields = [
        "mailing__message__subject",
        "status",
    ]  # Поиск по теме сообщения рассылки и статусу
