from django.contrib import admin
from .models import Product, BlogPost, Version

# Регистрация модели Product
admin.site.register(Product)

# Регистрация модели BlogPost
admin.site.register(BlogPost)

# Регистрация модели Version
# Добавьте эту строку для регистрации модели Version
admin.site.register(Version)
