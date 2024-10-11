from django.urls import path
from . import views

app_name = "mailing_service"

urlpatterns = [
    path("", views.mailing_list, name="mailing_list"),  # Список рассылок
    path("create/", views.mailing_create, name="mailing_create"),  # Создание рассылки
    path(
        "<int:pk>/", views.mailing_detail, name="mailing_detail"
    ),  # Просмотр деталей рассылки
    path(
        "<int:pk>/update/", views.mailing_update, name="mailing_update"
    ),  # Редактирование рассылки
    path(
        "<int:pk>/delete/", views.mailing_delete, name="mailing_delete"
    ),  # Удаление рассылки
    path("report/", views.mailing_report, name="mailing_report"),  # Отчет о рассылках
]
