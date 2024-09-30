from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from products.models import Version
from products.forms import VersionForm


# Создание новой версии продукта
class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'products/version_form.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        product = form.cleaned_data['product']
        # Деактивируем предыдущую активную версию, если она существует
        Version.objects.filter(product=product, is_current_version=True).update(is_current_version=False)
        return super().form_valid(form)


# Обновление версии продукта
class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'products/version_form.html'

    def form_valid(self, form):
        product = form.cleaned_data['product']
        # Деактивируем предыдущую активную версию, если новая версия становится активной
        is_current = form.cleaned_data.get('is_current_version', False)
        if is_current:
            Version.objects.filter(product=product, is_current_version=True).update(is_current_version=False)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('homepage')


# Удаление версии продукта
class VersionDeleteView(DeleteView):
    model = Version
    template_name = 'products/version_confirm_delete.html'
    success_url = reverse_lazy('homepage')


# Класс для установки активной версии
class SetActiveVersionView(View):
    def post(self, request, *args, **kwargs):
        version_id = request.POST.get('active_version')
        version = get_object_or_404(Version, pk=version_id)

        # Деактивируем предыдущую активную версию
        Version.objects.filter(product=version.product, is_current_version=True).update(is_current_version=False)

        # Устанавливаем текущую версию
        version.is_current_version = True
        version.save()

        return redirect('homepage')  # Перенаправляем на главную страницу
