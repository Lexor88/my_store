import re  # Для регулярных выражений
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Создание обычного пользователя."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Установка пароля
        user.is_active = True  # Убедитесь, что пользователь активен
        user.save(using=self._db)  # Сохранение пользователя в базе данных
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя."""
        extra_fields.setdefault("is_staff", True)  # Суперпользователь имеет доступ в админку
        extra_fields.setdefault("is_superuser", True)  # У суперпользователя есть все права
        extra_fields.setdefault("is_active", True)  # Убедитесь, что суперпользователь активен
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя."""
    email = models.EmailField(unique=True)  # Уникальный адрес электронной почты
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)  # Аватар пользователя
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Номер телефона
    country = models.CharField(max_length=100, null=True, blank=True)  # Страна пользователя

    is_active = models.BooleanField(default=True)  # По умолчанию юзер активен
    is_staff = models.BooleanField(default=False)  # Может ли пользователь заходить в админку

    objects = UserManager()  # Присваиваем менеджер

    USERNAME_FIELD = "email"  # Поле, которое будет использоваться для аутентификации
    REQUIRED_FIELDS = []  # Поля, которые должны быть указаны при создании пользователя

    def __str__(self):
        """Удобное представление пользователя."""
        return self.email

    def clean(self):
        """Валидация данных перед сохранением."""
        # Валидация номера телефона
        if self.phone_number and not re.match(r"^\+?1?\d{9,15}$", self.phone_number):
            raise ValidationError(
                "Неверный формат номера телефона. Используйте формат: +1234567890 или 1234567890."
            )

        # Валидация страны
        if self.country and len(self.country) < 2:
            raise ValidationError("Страна должна содержать как минимум 2 символа.")
