from django.urls import path
from .views import (
    register,
    CustomLoginView,
    reset_password,
    edit_profile,
    verify_email,
    email_sent,  # Добавляем представление email_sent
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
    path(
        "email-sent/", email_sent, name="email_sent"
    ),  # Добавляем этот маршрут
]
