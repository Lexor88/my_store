from django.views.generic import TemplateView


# Контроллер для страницы контактов
class ContactView(TemplateView):
    template_name = "products/contact.html"
