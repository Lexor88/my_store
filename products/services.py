# products/services.py
from django.core.cache import cache
from products.models import Category


def get_categories():
    # Проверяем, есть ли список категорий в кеше
    categories = cache.get("categories_list")

    if not categories:
        # Если нет в кеше, получаем из базы данных и сохраняем в кеше
        categories = Category.objects.all()
        cache.set(
            "categories_list", categories, 60 * 15
        )  # Кешируем список категорий на 15 минут

    return categories
