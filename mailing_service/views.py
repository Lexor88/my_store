from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Mailing
from .forms import MailingForm
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User


# Список рассылок
@cache_page(60 * 15)  # Кешировать на 15 минут
@login_required
def mailing_list(request):
    if request.user.is_staff:
        mailings = Mailing.objects.all()  # Менеджеры видят все рассылки
    else:
        mailings = Mailing.objects.filter(
            owner=request.user
        )  # Пользователи видят только свои рассылки
    return render(request, "mailing_service/mailing_list.html", {"mailings": mailings})


# Просмотр деталей рассылки
@cache_page(60 * 15)  # Кешировать на 15 минут
@login_required
def mailing_detail(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if not (request.user.is_staff or mailing.owner == request.user):
        return redirect(
            "mailing_service:mailing_list"
        )  # Запретить доступ к чужим рассылкам
    return render(request, "mailing_service/mailing_detail.html", {"mailing": mailing})


# Создание новой рассылки
@cache_page(60 * 15)  # Кешировать на 15 минут
@login_required
def mailing_create(request):
    if request.method == "POST":
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.owner = request.user  # Привязываем рассылку к текущему пользователю
            mailing.save()
            messages.success(request, "Рассылка успешно создана!")
            return redirect("mailing_service:mailing_list")
        else:
            messages.error(
                request,
                "Ошибка при создании рассылки. Проверьте корректность введенных данных.",
            )
    else:
        form = MailingForm()
    return render(request, "mailing_service/mailing_form.html", {"form": form})


# Редактирование рассылки
@cache_page(60 * 15)  # Кешировать на 15 минут
@login_required
def mailing_update(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if not (request.user.is_staff or mailing.owner == request.user):
        return redirect(
            "mailing_service:mailing_list"
        )  # Запретить доступ к чужим рассылкам
    if request.method == "POST":
        form = MailingForm(request.POST, instance=mailing)
        if form.is_valid():
            form.save()
            messages.success(request, "Рассылка успешно обновлена!")
            return redirect("mailing_service:mailing_detail", pk=pk)
        else:
            messages.error(
                request,
                "Ошибка при обновлении рассылки. Проверьте корректность введенных данных.",
            )
    else:
        form = MailingForm(instance=mailing)
    return render(request, "mailing_service/mailing_form.html", {"form": form})


# Удаление рассылки
@cache_page(60 * 15)  # Кешировать на 15 минут
@login_required
def mailing_delete(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if not (request.user.is_staff or mailing.owner == request.user):
        return redirect(
            "mailing_service:mailing_list"
        )  # Запретить доступ к чужим рассылкам
    if request.method == "POST":
        mailing.delete()
        messages.success(request, "Рассылка успешно удалена!")
        return redirect("mailing_service:mailing_list")

    # Запрос подтверждения удаления
    return render(
        request, "mailing_service/mailing_confirm_delete.html", {"mailing": mailing}
    )


# Дашборд для менеджеров
@cache_page(60 * 15)  # Кешировать на 15 минут
@user_passes_test(lambda u: u.is_staff)  # Доступ только для менеджеров
def manager_dashboard(request):
    mailings = Mailing.objects.all()  # Менеджер видит все рассылки
    users = User.objects.all()  # Менеджер видит всех пользователей
    return render(
        request, "manager/dashboard.html", {"mailings": mailings, "users": users}
    )


# Отчет проведенных рассылок
@login_required
def mailing_report(request):
    mailings = Mailing.objects.filter(
        owner=request.user
    )  # Получаем рассылки текущего пользователя
    return render(
        request, "mailing_service/mailing_report.html", {"mailings": mailings}
    )
