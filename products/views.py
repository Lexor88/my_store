from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'object': product}
    return render(request, 'products/product_detail.html', context)

def homepage(request):
    products = Product.objects.all()  # Получаем все товары из базы данных
    context = {'products': products}  # Передаем список товаров в шаблон
    return render(request, 'products/homepage.html', context)