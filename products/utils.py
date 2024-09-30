# products/utils.py
from django.core.mail import send_mail
from django.conf import settings


def send_letter_about_reaching_certain_number_of_views(blog_id: int, views_count: int):
    send_mail(
        'Поздравляем! Количество просмотров',
        f'Ваша статья с ID {blog_id} достигла {views_count} просмотров!',
        settings.DEFAULT_FROM_EMAIL,
        ['maksimleksin88@yandex.ru'],  # email здесь
        fail_silently=False,
    )
