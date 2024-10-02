from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
    ContactView,
    VersionCreateView,
    VersionUpdateView,
    VersionDeleteView,
    SetActiveVersionView,
)

urlpatterns = [
    # Главная страница (без префикса 'products/')
    path("", ProductListView.as_view(), name="homepage"),
    # Маршруты для товаров
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/add/", ProductCreateView.as_view(), name="add_product"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="edit_product"),
    # Редактирование товара
    path(
        "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="delete_product"
    ),
    # Удаление товара
    # Маршруты для блога
    path("blog/", BlogPostListView.as_view(), name="blog_list"),
    path("blog/create/", BlogPostCreateView.as_view(), name="blog_create"),
    path("blog/<slug:slug>/", BlogPostDetailView.as_view(), name="blog_detail"),
    path("blog/<slug:slug>/update/", BlogPostUpdateView.as_view(), name="blog_update"),
    path("blog/<slug:slug>/delete/", BlogPostDeleteView.as_view(), name="blog_delete"),
    # Маршрут для страницы контактов
    path("contact/", ContactView.as_view(), name="contact"),
    # Маршруты для версий продукта
    path("version/add/", VersionCreateView.as_view(), name="add_version"),
    # Создание новой версии
    path("version/<int:pk>/edit/", VersionUpdateView.as_view(), name="edit_version"),
    # Редактирование версии
    path(
        "version/<int:pk>/delete/", VersionDeleteView.as_view(), name="delete_version"
    ),
    # Удаление версии
    # Маршрут для установки активной версии
    path(
        "set_active_version/", SetActiveVersionView.as_view(), name="set_active_version"
    ),
    # Добавляем маршрут
]
