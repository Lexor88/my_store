from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Импорт вашей кастомной модели пользователя
from .forms import CustomUserChangeForm, UserRegistrationForm


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = UserRegistrationForm  # Используем форму для регистрации нового пользователя

    model = User
    list_display = (
        "email",
        "phone_number",
        "country",
        "is_staff",
        "is_active",
    )
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "avatar",
                    "phone_number",
                    "country",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",  # Разрешаем добавлять группы при создании пользователя
                ),
            },
        ),
    )

    # Устанавливаем поля для изменения и добавления пользователей в админке
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


# Отменяем регистрацию стандартного UserAdmin, если он был зарегистрирован
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Регистрируем кастомную модель пользователя с новой формой администрирования
admin.site.register(User, CustomUserAdmin)
