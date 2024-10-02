from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.utils.text import slugify
from smtplib import SMTPException
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from products.models import Product, BlogPost, Version
from products.forms import ProductForm, BlogPostForm, VersionForm
from products.utils import send_letter_about_reaching_certain_number_of_views


# Контроллер для страницы контактов
class ContactView(TemplateView):
    template_name = "products/contact.html"


# Отображение списка блогов
class BlogPostListView(ListView):
    model = BlogPost
    template_name = "products/blog_list.html"
    context_object_name = "blog_posts"
    paginate_by = 5

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by("-created_at")


# Детальное отображение блога с увеличением счетчика просмотров
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "products/blog_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()

        if obj.views == 100:
            try:
                send_letter_about_reaching_certain_number_of_views(obj.id, obj.views)
            except SMTPException as e:
                messages.error(self.request, f"Ошибка SMTP при отправке письма: {e}")
            except Exception as e:
                messages.error(self.request, f"Общая ошибка при отправке письма: {e}")

        return obj


# Создание нового блога
class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "products/blog_form.html"
    success_url = reverse_lazy("blog_list")

    def form_valid(self, form):
        blog_post = form.save(commit=False)
        blog_post.slug = slugify(blog_post.title)
        blog_post.save()
        messages.success(self.request, "Блог успешно создан!")
        return super().form_valid(form)


# Редактирование блога
class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "products/blog_form.html"

    def get_success_url(self):
        messages.success(self.request, "Блог успешно обновлен!")
        return reverse_lazy("blog_detail", kwargs={"slug": self.object.slug})


# Удаление блога
class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "products/blog_confirm_delete.html"
    success_url = reverse_lazy("blog_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Блог успешно удален!")
        return super().delete(request, *args, **kwargs)


# Отображение главной страницы с товарами
class ProductListView(ListView):
    model = Product
    template_name = "products/homepage.html"
    context_object_name = "products"
    paginate_by = 3  # Количество товаров на одной странице

    def get_queryset(self):
        return Product.objects.all().order_by("name")

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
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Продукт успешно создан!")
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Для создания продукта войдите в учетную запись.")
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)


# Обновление продукта
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/add_product.html"

    def get_success_url(self):
        messages.success(self.request, "Продукт успешно обновлен!")
        return reverse_lazy("product_detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            messages.error(request, "Вы не можете редактировать этот продукт.")
            return redirect("homepage")
        return super().dispatch(request, *args, **kwargs)


# Удаление продукта
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("homepage")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            messages.error(request, "Вы не можете удалить этот продукт.")
            return redirect("homepage")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Продукт успешно удален!")
        return super().delete(request, *args, **kwargs)


# Создание новой версии продукта
class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = "products/version_form.html"
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        product = form.cleaned_data["product"]
        Version.objects.filter(product=product, is_current_version=True).update(is_current_version=False)
        messages.success(self.request, "Новая версия продукта успешно создана!")
        return super().form_valid(form)


# Обновление версии продукта
class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    template_name = "products/version_form.html"

    def form_valid(self, form):
        product = form.cleaned_data["product"]
        is_current = form.cleaned_data.get("is_current_version", False)
        if is_current:
            Version.objects.filter(product=product, is_current_version=True).update(is_current_version=False)
        messages.success(self.request, "Версия продукта успешно обновлена!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("homepage")


# Удаление версии продукта
class VersionDeleteView(DeleteView):
    model = Version
    template_name = "products/version_confirm_delete.html"
    success_url = reverse_lazy("homepage")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Версия продукта успешно удалена!")
        return super().delete(request, *args, **kwargs)


# Класс для установки активной версии
class SetActiveVersionView(View):
    def post(self, request, *args, **kwargs):
        version_id = request.POST.get("active_version")
        version = get_object_or_404(Version, pk=version_id)

        # Сбросить текущую версию для всех остальных версий продукта
        Version.objects.filter(product=version.product, is_current_version=True).update(is_current_version=False)

        # Установить новую текущую версию
        version.is_current_version = True
        version.save()

        messages.success(request, "Активная версия успешно установлена!")
        return redirect("homepage")
