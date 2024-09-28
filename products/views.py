# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.core.paginator import Paginator

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'object': product}
    return render(request, 'products/product_detail.html', context)

def homepage(request):
    # Добавляем сортировку товаров по ID, чтобы избежать предупреждения об отсутствии порядка
    product_list = Product.objects.all().order_by('id')
    paginator = Paginator(product_list, 5)  # 5 продуктов на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Передаем объект пагинации в контекст
    return render(request, 'products/homepage.html', {'products': page_obj})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')  # Перенаправляем на главную после успешного добавления
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})
