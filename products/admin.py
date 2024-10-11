from django.contrib import admin
from .models import Product, BlogPost, Version


# Кастомный админ-класс для модели Product
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "is_published",
        "created_at",
    )  # Поля, отображаемые в списке
    search_fields = ("name", "description")  # Поиск по имени и описанию
    list_filter = (
        "is_published",
        "created_at",
    )  # Фильтры по статусу публикации и дате создания
    prepopulated_fields = {
        "slug": ("name",)
    }  # Предзаполнение поля slug на основе имени

    def get_queryset(self, request):
        # Переопределение метода для управления видимостью продуктов в админке
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Суперпользователи видят все продукты
        return qs.filter(
            owner=request.user
        )  # Обычные пользователи видят только свои продукты


# Кастомный админ-класс для модели BlogPost
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_published",
        "created_at",
    )  # Поля, отображаемые в списке
    search_fields = ("title", "content")  # Поиск по заголовку и содержимому
    list_filter = (
        "is_published",
        "created_at",
    )  # Фильтры по статусу публикации и дате создания


# Кастомный админ-класс для модели Version
class VersionAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "version_name",
        "version_number",
        "is_current_version",
    )  # Поля, отображаемые в списке
    search_fields = ("version_name",)  # Поиск по названию версии
    list_filter = ("is_current_version",)  # Фильтр по статусу текущей версии


# Регистрация моделей с кастомными админ-классами
admin.site.register(Product, ProductAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Version, VersionAdmin)
