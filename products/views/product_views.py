from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from products.models import Product
from products.forms import ProductForm


# Отображение главной страницы с товарами
class ProductListView(ListView):
    model = Product
    template_name = 'products/homepage.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.order_by('id')  # Упорядочивание по id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Загружаем версии для каждого продукта
        for product in context['products']:
            # Находим активную версию
            product.active_version = product.versions.filter(is_current_version=True).first()
        return context


# Детальное отображение продукта
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'


# Создание нового продукта
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/add_product.html'
    success_url = reverse_lazy('homepage')


# Обновление продукта
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/add_product.html'

    def get_success_url(self):
        return reverse_lazy('product_detail',
                            kwargs={'pk': self.object.pk})  # Перенаправление на страницу продукта после обновления


# Удаление продукта
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('homepage')  # Перенаправление на главную страницу после удаления
