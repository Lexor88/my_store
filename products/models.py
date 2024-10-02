from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from users.models import User  # Импортируем модель пользователя


# Модель товаров
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.CharField(max_length=100, default='Uncategorized')  # По умолчанию
    created_at = models.DateTimeField(auto_now_add=True)  # Устанавливаем текущее время при создании объекта
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего изменения
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')  # Связь с пользователем

    def __str__(self):
        return self.name

    def clean(self):
        # Проверка цены перед сохранением
        if self.price < 0:
            raise ValidationError("Цена не может быть отрицательной.")

    def save(self, *args, **kwargs):
        self.clean()  # Проверка перед сохранением
        super().save(*args, **kwargs)


# Модель блога
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    preview_image = models.ImageField(upload_to="blog_previews/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.title)

    def save(self, *args, **kwargs):
        self.clean()  # Убедитесь, что slug установлен перед сохранением
        super().save(*args, **kwargs)


class Version(models.Model):
    product = models.ForeignKey(
        Product, related_name="versions", on_delete=models.CASCADE
    )
    version_name = models.CharField(max_length=100)  # Название версии
    version_number = models.CharField(max_length=10)  # Номер версии
    is_current_version = models.BooleanField(default=False)  # Признак текущей версии

    def __str__(self):
        return f"{self.version_name} (v{self.version_number})"
