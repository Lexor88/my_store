from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Главная страница
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_product/', views.add_product, name='add_product'),  # Новый URL для добавления продукта
]
