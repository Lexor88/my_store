from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),  # Подключение админки
    path(
        "", include("products.urls")
    ),  # Подключаем маршруты из приложения products
    path(
        "users/", include("users.urls")
    ),  # Подключаем маршруты из приложения users
]

# Добавляем поддержку медиафайлов и статических файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )  # Подключаем статические файлы
