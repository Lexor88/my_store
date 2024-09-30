from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductCreateView,
    BlogPostListView, BlogPostDetailView, BlogPostCreateView,
    BlogPostUpdateView, BlogPostDeleteView, ContactView  # Импортируйте ContactView
)

urlpatterns = [
    # Маршруты для товаров
    path('', ProductListView.as_view(), name='homepage'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),

    # Маршруты для блога
    path('blog/', BlogPostListView.as_view(), name='blog_list'),
    path('blog/create/', BlogPostCreateView.as_view(), name='blog_create'),

    # Этот маршрут должен быть перед 'blog/<slug:slug>/'
    path('blog/<slug:slug>/', BlogPostDetailView.as_view(), name='blog_detail'),
    path('blog/<slug:slug>/update/', BlogPostUpdateView.as_view(), name='blog_update'),
    path('blog/<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='blog_delete'),

    # Маршрут для страницы контактов
    path('contact/', ContactView.as_view(), name='contact'),  # Добавьте этот маршрут
]
