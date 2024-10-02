from django.urls import path
from .views import register, CustomLoginView, reset_password, edit_profile
from django.contrib.auth.views import LogoutView  # Импортируем LogoutView

urlpatterns = [
    path('register/', register, name='register'),  # Маршрут для регистрации
    path('login/', CustomLoginView.as_view(), name='login'),  # Маршрут для авторизации
    path('reset_password/', reset_password, name='reset_password'),  # Маршрут для восстановления пароля
    path('profile/edit/', edit_profile, name='edit_profile'),  # Маршрут для редактирования профиля
    path('logout/', LogoutView.as_view(), name='logout'),  # Маршрут для выхода
]
