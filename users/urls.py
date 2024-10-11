from django.urls import path
from .views import (
    register,
    CustomLoginView,
    reset_password,
    edit_profile,
    verify_email,
    email_sent,
    user_create,  # Добавляем представление для создания пользователя
    user_list,    # Добавляем представление для списка пользователей
    user_delete,  # Добавляем представление для удаления пользователя
    user_update,  # Добавляем представление для редактирования пользователя
)
from django.contrib.auth.views import LogoutView

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("reset_password/", reset_password, name="reset_password"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("verify-email/<uidb64>/<token>/", verify_email, name="verify_email"),
    path("email-sent/", email_sent, name="email_sent"),
    path("create/", user_create, name="user_create"),  # Создание пользователя
    path("list/", user_list, name="user_list"),        # Список пользователей
    path("<int:pk>/delete/", user_delete, name="user_delete"),  # Удаление пользователя
    path("<int:pk>/update/", user_update, name="user_update"),  # Редактирование пользователя
]
