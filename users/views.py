from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm, CustomUserChangeForm
from .models import User
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
import random
import string


# Кастомная страница входа
class CustomLoginView(LoginView):
    template_name = "users/login.html"


# Регистрация пользователя
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Проверка на существование пользователя
            if User.objects.filter(email=form.cleaned_data["email"]).exists():
                messages.error(request, "Пользователь с таким email уже существует.")
                return redirect("users:register")

            user = form.save(commit=False)
            user.is_active = (
                False  # Делаем пользователя неактивным до подтверждения email
            )
            user.save()

            # Отправляем письмо для подтверждения email
            current_site = get_current_site(request)
            subject = "Подтверждение вашей электронной почты"
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            message = render_to_string(
                "users/email_confirmation.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": uid,
                    "token": token,
                },
            )

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            messages.info(
                request,
                "На ваш email отправлено письмо для подтверждения. Проверьте свою почту.",
            )
            return redirect(
                "users:email_sent"
            )  # Перенаправляем на страницу с уведомлением об отправке email
    else:
        form = UserRegistrationForm()

    return render(request, "users/register.html", {"form": form})


# Верификация email
def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Активируем пользователя
        user.is_active = True
        user.save()

        messages.success(
            request, "Ваш email успешно подтвержден. Теперь вы можете войти в систему."
        )
        return redirect("users:login")
    else:
        messages.error(
            request, "Ссылка для подтверждения недействительна или устарела."
        )
        return redirect("users:register")


# Редактирование профиля
@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен!")
            return redirect("users:edit_profile")
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, "users/edit_profile.html", {"form": form})


# Сброс пароля
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
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "Новый пароль отправлен на вашу почту.")
        except User.DoesNotExist:
            messages.error(request, "Пользователь с таким email не найден.")
        return redirect("users:login")

    return render(request, "users/reset_password.html")


# Уведомление об отправке email
def email_sent(request):
    return render(request, "users/email_sent.html")


# Создание пользователя
@login_required
def user_create(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь с таким именем уже существует.")
            return redirect("users:user_create")

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        messages.success(request, "Пользователь успешно создан!")
        return redirect("users:user_list")
    return render(request, "users/user_form.html")


# Список пользователей
@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, "users/user_list.html", {"users": users})


# Удаление пользователя
@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, "Пользователь успешно удален!")
    return redirect("users:user_list")


# Редактирование пользователя
@login_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.save()
        messages.success(request, "Пользователь успешно обновлен!")
        return redirect("users:user_list")
    return render(request, "users/user_form.html", {"user": user})
