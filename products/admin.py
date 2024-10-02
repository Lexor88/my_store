from django.contrib import admin
from .models import Product, BlogPost, Version

# Кастомный админ-класс для модели Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_published', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_published', 'created_at')
    prepopulated_fields = {'slug': ('name',)}  # Предзаполнение поля slug

# Кастомный админ-класс для модели BlogPost
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('is_published', 'created_at')

# Кастомный админ-класс для модели Version
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version_name', 'version_number', 'is_current_version')
    search_fields = ('version_name',)
    list_filter = ('is_current_version',)

# Регистрация моделей с кастомными админ-классами
admin.site.register(Product, ProductAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Version, VersionAdmin)
