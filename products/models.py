from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

# Модель товаров
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL-адрес")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to="product_images/", blank=True, null=True, verbose_name="Изображение")
    category = models.CharField(max_length=100, default="Uncategorized", verbose_name="Категория")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products", verbose_name="Владелец")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")

    class Meta:
        permissions = [
            ("can_publish_product", "Can publish/unpublish product"),
            ("can_change_description", "Can change product description"),
            ("can_change_category", "Can change product category"),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        # Проверка уникальности slug перед сохранением
        if not self.slug:  # Проверяем только если slug не установлен
            self.slug = slugify(self.name)  # Генерируем slug
        if Product.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            raise ValidationError("Продукт с таким URL-адресом уже существует.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Запускаем полную валидацию модели перед сохранением
        super().save(*args, **kwargs)

    @property
    def active_version(self):
        # Используем свойство только для получения текущей версии продукта
        return self.versions.filter(is_current_version=True).first()

# Модель блога
class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL-адрес")
    content = models.TextField(verbose_name="Содержание")
    preview_image = models.ImageField(upload_to="blog_previews/", null=True, blank=True, verbose_name="Изображение превью")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return self.title

    def clean(self):
        forbidden_words = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]
        for word in forbidden_words:
            if word in self.title.lower():
                raise ValidationError(f"Использование слова '{word}' в заголовке запрещено.")
        # Проверка уникальности slug перед сохранением
        if not self.slug:  # Проверяем только если slug не установлен
            self.slug = slugify(self.title)  # Генерируем slug
        if BlogPost.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            raise ValidationError("Блог с таким URL-адресом уже существует.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Запускаем полную валидацию модели перед сохранением
        super().save(*args, **kwargs)

    class Meta:
        permissions = [
            ("can_manage_blog", "Can manage blog posts"),
        ]

# Модель версий продукта
class Version(models.Model):
    product = models.ForeignKey(Product, related_name="versions", on_delete=models.CASCADE, verbose_name="Продукт")
    version_name = models.CharField(max_length=100, verbose_name="Название версии")
    version_number = models.CharField(max_length=10, verbose_name="Номер версии")
    is_current_version = models.BooleanField(default=False, verbose_name="Текущая версия")

    def __str__(self):
        return f"{self.version_name} (v{self.version_number})"

    def clean(self):
        # Убедимся, что только одна версия продукта отмечена как текущая
        if self.is_current_version:
            Version.objects.filter(product=self.product).update(is_current_version=False)

    def save(self, *args, **kwargs):
        self.full_clean()  # Запускаем полную валидацию модели перед сохранением
        super().save(*args, **kwargs)

# Модель категорий
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="URL-адрес категории")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Проверяем только если slug не установлен
            self.slug = slugify(self.name)  # Генерируем slug
        super().save(*args, **kwargs)
