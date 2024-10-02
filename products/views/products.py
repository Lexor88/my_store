from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from products.models import Product
from products.forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404


# Отображение главной страницы с товарами
class ProductListView(ListView):
    model = Product
    template_name = "products/homepage.html"
    context_object_name = "products"
    paginate_by = 3

    def get_queryset(self):
        """Показываем все продукты для авторизованных пользователей, только опубликованные для неавторизованных."""
        if self.request.user.is_authenticated:
            return Product.objects.all().order_by("name")
        else:
            return Product.objects.filter(is_published=True).order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context["products"]:
            product.active_version = product.versions.filter(is_current_version=True).first()
        return context


# Детальное отображение продукта
class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"


# Создание нового продукта
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/add_product.html"
    success_url = reverse_lazy("homepage")

    def get_form_kwargs(self):
        """Передаем текущего пользователя в форму."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Устанавливаем владельца продукта и отправляем сообщение об успехе."""
        form.instance.owner = self.request.user
        messages.success(self.request, "Продукт успешно создан!")
        return super().form_valid(form)


# Обновление продукта
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/add_product.html"

    def test_func(self):
        """Проверяем, имеет ли пользователь права на редактирование продукта."""
        product = self.get_object()  # Получаем объект продукта
        return self.request.user == product.owner or self.request.user.has_perm('products.can_change_product')

    def get_success_url(self):
        """Возвращаем URL для перенаправления после успешного обновления."""
        messages.success(self.request, "Продукт успешно обновлен!")
        return reverse_lazy("product_detail", kwargs={"slug": self.object.slug})  # Убедитесь, что slug работает

    def get_form_kwargs(self):
        """Передаем текущего пользователя в форму."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # Передаем пользователя в форму
        return kwargs


# Удаление продукта
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("homepage")

    def test_func(self):
        """Проверяем, имеет ли пользователь права на удаление продукта."""
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm('products.can_delete_product')

    def delete(self, request, *args, **kwargs):
        """Удаляем продукт и отправляем сообщение об успехе."""
        messages.success(request, "Продукт успешно удален!")
        return super().delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Проверяем статус публикации для обычных пользователей."""
        product = super().get_object(queryset)
        if not product.is_published and not (
                self.request.user.has_perm('products.can_publish_product') or self.request.user == product.owner):
            raise Http404("Этот продукт не опубликован.")
        return product


@login_required
def publish_product(request, pk):
    """Переключаем статус публикации продукта."""
    product = get_object_or_404(Product, pk=pk)
    if not request.user.has_perm('products.can_publish_product'):
        return HttpResponseForbidden("У вас нет прав на изменение статуса публикации.")

    product.is_published = not product.is_published
    product.save()
    messages.success(request, "Статус публикации продукта изменен.")
    return redirect('product_detail', slug=product.slug)
