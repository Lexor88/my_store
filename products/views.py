from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView, TemplateView
)
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException

from .models import Product, BlogPost
from .forms import ProductForm, BlogPostForm
from .utils import send_letter_about_reaching_certain_number_of_views  # Импортируем функцию


# Отображение главной страницы с товарами
class ProductListView(ListView):
    model = Product
    template_name = 'products/homepage.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.order_by('id')  # Упорядочивание по id


# Контроллер для страницы контактов
class ContactView(TemplateView):
    template_name = 'products/contact.html'  # Убедитесь, что этот шаблон существует


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


# Отображение списка блогов
class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'products/blog_list.html'
    context_object_name = 'blog_posts'
    paginate_by = 5

    # Фильтрация только опубликованных блогов
    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')  # Упорядочивание по дате создания


# Детальное отображение блога с увеличением счетчика просмотров
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'products/blog_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()

        print(f"Просмотры: {obj.views}")  # сообщение для проверки количества просмотров

        if obj.views == 100:
            print("Достигнуто 100 просмотров. Попытка отправить письмо...")
            try:
                send_letter_about_reaching_certain_number_of_views(obj.id, obj.views)
                print("Письмо успешно отправлено.")
            except SMTPException as e:
                print(f"Ошибка SMTP при отправке письма: {e}")
            except Exception as e:
                print(f"Общая ошибка при отправке письма: {e}")

        return obj


# Создание нового блога
class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'products/blog_form.html'
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        blog_post = form.save(commit=False)
        blog_post.slug = slugify(blog_post.title)
        blog_post.save()
        return super().form_valid(form)


# Редактирование блога
class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'products/blog_form.html'

    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'slug': self.object.slug})


# Удаление блога
class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'products/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')
