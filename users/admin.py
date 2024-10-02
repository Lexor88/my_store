from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User  # Импорт вашей кастомной модели пользователя
from .forms import CustomUserChangeForm, UserRegistrationForm

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = UserRegistrationForm  # Используем форму для регистрации нового пользователя

    model = User
    list_display = ("email", "phone_number", "country", "is_staff", "is_active")
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password", "avatar", "phone_number", "country")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )

# Отменяем регистрацию стандартного UserAdmin, если он был зарегистрирован
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Регистрируем новый админ с кастомной формой
admin.site.register(User, CustomUserAdmin)
