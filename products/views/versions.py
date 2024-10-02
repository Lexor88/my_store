from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from products.models import Version
from products.forms import VersionForm


# Создание новой версии продукта
class VersionCreateView(LoginRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    template_name = "products/version_form.html"
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        product = form.cleaned_data["product"]
        # Снять отметку с текущей версии, если есть
        Version.objects.filter(
            product=product, is_current_version=True
        ).update(is_current_version=False)
        messages.success(
            self.request, "Новая версия продукта успешно создана!"
        )
        return super().form_valid(form)


# Обновление версии продукта
class VersionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Version
    form_class = VersionForm
    template_name = "products/version_form.html"

    def test_func(self):
        version = self.get_object()
        # Проверяем права доступа: либо пользователь имеет специальное разрешение, либо он владелец продукта
        return (
            self.request.user.has_perm("products.can_change_version")
            or self.request.user == version.product.owner
        )

    def form_valid(self, form):
        product = form.cleaned_data["product"]
        is_current = form.cleaned_data.get("is_current_version", False)
        if is_current:
            Version.objects.filter(
                product=product, is_current_version=True
            ).update(is_current_version=False)
        messages.success(self.request, "Версия продукта успешно обновлена!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "products:product_detail", slug=self.object.product.slug
        )


# Удаление версии продукта
class VersionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Version
    template_name = "products/version_confirm_delete.html"
    success_url = reverse_lazy("homepage")

    def test_func(self):
        version = self.get_object()
        # Проверяем права доступа: либо пользователь имеет специальное разрешение, либо он владелец продукта
        return (
            self.request.user.has_perm("products.can_delete_version")
            or self.request.user == version.product.owner
        )

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Версия продукта успешно удалена!")
        return super().delete(request, *args, **kwargs)


# Класс для установки активной версии
class SetActiveVersionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        version_id = request.POST.get("active_version")
        if not version_id:
            messages.error(request, "ID версии не указан.")
            return redirect("homepage")

        version = get_object_or_404(Version, pk=version_id)

        if (
            not request.user.has_perm("products.can_change_version")
            and request.user != version.product.owner
        ):
            return HttpResponseForbidden("У вас нет прав на изменение версии.")

        # Установить все версии продукта как неактивные
        Version.objects.filter(product=version.product).update(
            is_current_version=False
        )

        # Установить выбранную версию как активную
        version.is_current_version = True
        version.save()

        messages.success(request, "Активная версия успешно установлена!")
        return redirect("products:product_detail", slug=version.product.slug)
