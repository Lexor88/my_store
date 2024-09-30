from django.db import models
from django.utils.text import slugify


# Модель товаров
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.CharField(max_length=100, default='Uncategorized')  # По умолчанию

    def __str__(self):
        return self.name


# Модель блога
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True, blank=True)  # Изменено на CharField
    content = models.TextField()
    preview_image = models.ImageField(upload_to='blog_previews/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)  # Добавляем поле is_published
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=50)
    version_name = models.CharField(max_length=100)
    is_current_version = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.version_name} (v{self.version_number})"
