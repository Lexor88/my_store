from django.contrib import admin
from .models import Product, BlogPost

# Регистрация модели Product (если еще не зарегистрирована)
admin.site.register(Product)

# Регистрация модели BlogPost
admin.site.register(BlogPost)
