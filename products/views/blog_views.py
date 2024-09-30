from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.text import slugify
from django.core.mail import send_mail
from smtplib import SMTPException
from products.models import BlogPost
from products.forms import BlogPostForm
from products.utils import send_letter_about_reaching_certain_number_of_views


# Отображение списка блогов
class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'products/blog_list.html'
    context_object_name = 'blog_posts'
    paginate_by = 5

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


# Детальное отображение блога с увеличением счетчика просмотров
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'products/blog_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        print(f"Просмотры: {obj.views}")

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
