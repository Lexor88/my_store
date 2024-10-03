"""
URL configuration for the my_store project.
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.decorators.cache import cache_page
from products.views import ProductDetailView  # Импортируем ProductDetailView

urlpatterns = [
    path("admin/", admin.site.urls),  # Подключение админки
    path("", include("products.urls")),  # Подключаем маршруты из приложения products
    path("users/", include("users.urls")),  # Подключаем маршруты из приложения users
    path(
        "product/<slug:slug>/",
        cache_page(60 * 15)(ProductDetailView.as_view()),
        name="product_detail",
    ),  # Добавляем кеширование
]

# Добавляем поддержку медиафайлов и статических файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
