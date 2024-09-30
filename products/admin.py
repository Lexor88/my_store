from django.contrib import admin
from .models import Product, BlogPost, Version  # Не забудьте импортировать модель Version

# Регистрация модели Product
admin.site.register(Product)

# Регистрация модели BlogPost
admin.site.register(BlogPost)

# Регистрация модели Version
admin.site.register(Version)  # Добавьте эту строку для регистрации модели Version
