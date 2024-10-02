from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegistrationForm
from .models import User
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
import random
import string


class CustomLoginView(LoginView):
    template_name = "users/login.html"


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                send_mail(
                    "Подтверждение регистрации",
                    "Вы успешно зарегистрировались!",
                    "maksimleksin88@yandex.ru",
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, "Вы успешно зарегистрированы!")
                return redirect("homepage")
            except Exception as e:
                messages.error(request, f"Ошибка регистрации: {e}")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = UserRegistrationForm()

    return render(request, "users/registration.html", {"form": form})


@login_required
def edit_profile(request):
    user = request.user
    # Если нужно использовать другую форму для редактирования профиля,
    # используйте UserEditForm
    form = UserRegistrationForm(instance=user)

    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен!")
            return redirect("homepage")

    return render(request, "users/edit_profile.html", {"form": form})


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            new_password = "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )
            user.set_password(new_password)
            user.save()
            send_mail(
                "Восстановление пароля",
                f"Ваш новый пароль: {new_password}",
                "maksimleksin88@yandex.ru",
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "Новый пароль отправлен на вашу почту.")
        except User.DoesNotExist:
            messages.error(request, "Пользователь с таким email не найден.")
        return redirect("login")

    return render(request, "users/reset_password.html")
