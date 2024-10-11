from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from products.models import Product
from products.forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404
from products.services import get_categories
from django.views.decorators.cache import cache_page
from mailing_service.models import Client, Mailing
from products.models import BlogPost


# Отображение главной страницы с товарами
class ProductListView(ListView):
    model = Product
    template_name = "products/homepage.html"
    context_object_name = "products"
    paginate_by = 3

    def get_queryset(self):
        """Показываем все продукты для авторизованных пользователей, только опубликованные для неавторизованных."""
        queryset = (
            Product.objects.all().order_by("name")
            if self.request.user.is_authenticated
            else Product.objects.filter(is_published=True).order_by("name")
        )

        # Получаем выбранную категорию из параметров запроса
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_with_versions = []

        for product in context["products"]:
            product_data = {
                "product": product,
                "active_version": product.active_version,
            }
            products_with_versions.append(product_data)

        context["mailings"] = Mailing.objects.all()  # Получаем все рассылки
        context["active_mailings_count"] = Mailing.objects.filter(
            status="running"
        ).count()
        context["total_mailings_count"] = Mailing.objects.count()
        context["unique_clients_count"] = (
            Client.objects.count()
        )  # Получаем количество уникальных клиентов
        context["products_with_versions"] = products_with_versions
        context["categories"] = get_categories()  # Добавляем категории в контекст
        context["selected_category"] = self.request.GET.get(
            "category", ""
        )  # Добавляем выбранную категорию

        # Получаем три случайные статьи из блога
        context["random_blog_posts"] = BlogPost.objects.order_by("?")[
            :3
        ]  # Добавляем три случайные статьи

        return context


# Кешируем детали продукта на 15 минут
@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        # Найти текущую версию продукта
        current_version = product.versions.filter(is_current_version=True).first()
        context["active_version"] = current_version
        return context


# Создание нового продукта
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/add_product.html"
    success_url = reverse_lazy("products:homepage")

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
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm(
            "products.can_change_product"
        )

    def get_success_url(self):
        """Возвращаем URL для перенаправления после успешного обновления."""
        messages.success(self.request, "Продукт успешно обновлен!")
        return reverse_lazy(
            "products:product_detail", kwargs={"slug": self.object.slug}
        )

    def get_form_kwargs(self):
        """Передаем текущего пользователя в форму."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


# Удаление продукта
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("products:homepage")

    def test_func(self):
        """Проверяем, имеет ли пользователь права на удаление продукта."""
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm(
            "products.can_delete_product"
        )

    def delete(self, request, *args, **kwargs):
        """Удаляем продукт и отправляем сообщение об успехе."""
        messages.success(request, "Продукт успешно удален!")
        return super().delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Проверяем статус публикации для обычных пользователей."""
        product = super().get_object(queryset)
        if not product.is_published and not (
            self.request.user.has_perm("products.can_publish_product")
            or self.request.user == product.owner
        ):
            raise Http404("Этот продукт не опубликован.")
        return product


@login_required
def publish_product(request, slug):
    """Переключаем статус публикации продукта."""
    product = get_object_or_404(Product, slug=slug)
    if not request.user.has_perm("products.can_publish_product"):
        return HttpResponseForbidden("У вас нет прав на изменение статуса публикации.")

    product.is_published = not product.is_published
    product.save()
    messages.success(request, "Статус публикации продукта изменен.")
    return redirect("products:product_detail", slug=product.slug)


# Список категорий
def category_list(request):
    categories = get_categories()
    return render(request, "products/category_list.html", {"categories": categories})
