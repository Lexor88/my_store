from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
import re  # Для регулярных выражений


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    is_active = models.BooleanField(default=False)  # По умолчанию юзер неактивен
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Поля, которые должны быть указаны при создании пользователя

    def __str__(self):
        return self.email  # Удобное представление пользователя

    def clean(self):
        # Валидация номера телефона
        if self.phone_number and not re.match(r"^\+?1?\d{9,15}$", self.phone_number):
            raise ValidationError(
                "Неверный формат номера телефона. Используйте формат: +1234567890 или 1234567890."
            )

        # Валидация страны
        if self.country and len(self.country) < 2:
            raise ValidationError("Страна должна содержать как минимум 2 символа.")
