from django.urls import path

# Импорт представлений из отдельных модулей
from .views.products import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    publish_product,
)
from .views.blog import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
)
from .views.versions import (
    VersionCreateView,
    VersionUpdateView,
    VersionDeleteView,
    SetActiveVersionView,
)
from .views.contact import ContactView

# Добавляем пространство имен для приложения 'products'
app_name = "products"

urlpatterns = [
    # Главная страница
    path("", ProductListView.as_view(), name="homepage"),
    # Маршрут для добавления товара (перемещен выше)
    path("products/add/", ProductCreateView.as_view(), name="add_product"),
    # Маршруты для товаров
    path(
        "products/<slug:slug>/",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "products/<slug:slug>/edit/",
        ProductUpdateView.as_view(),
        name="edit_product",
    ),
    path(
        "products/<slug:slug>/delete/",
        ProductDeleteView.as_view(),
        name="delete_product",
    ),
    path(
        "products/<slug:slug>/publish/",
        publish_product,
        name="publish_product",
    ),
    # Маршруты для блога
    path("blog/", BlogPostListView.as_view(), name="blog_list"),
    path("blog/create/", BlogPostCreateView.as_view(), name="blog_create"),
    path(
        "blog/<slug:slug>/", BlogPostDetailView.as_view(), name="blog_detail"
    ),
    path(
        "blog/<slug:slug>/update/",
        BlogPostUpdateView.as_view(),
        name="blog_update",
    ),
    path(
        "blog/<slug:slug>/delete/",
        BlogPostDeleteView.as_view(),
        name="blog_delete",
    ),
    # Маршрут для страницы контактов
    path("contact/", ContactView.as_view(), name="contact"),
    # Маршруты для версий продукта
    path("version/add/", VersionCreateView.as_view(), name="add_version"),
    path(
        "version/<slug:slug>/edit/",
        VersionUpdateView.as_view(),
        name="edit_version",
    ),  # Изменено на slug
    path(
        "version/<slug:slug>/delete/",
        VersionDeleteView.as_view(),
        name="delete_version",
    ),  # Изменено на slug
    # Маршрут для установки активной версии
    path(
        "set_active_version/",
        SetActiveVersionView.as_view(),
        name="set_active_version",
    ),
]
