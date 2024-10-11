from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserChangeForm, UserRegistrationForm


class CustomUserAdmin(UserAdmin):
    """Кастомный админ-класс для модели пользователя."""

    form = CustomUserChangeForm
    add_form = (
        UserRegistrationForm  # Используем форму для регистрации нового пользователя
    )

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
        (None, {"fields": ("email", "password", "avatar", "phone_number", "country")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
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
                    "groups",
                ),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        """Возвращает набор полей в зависимости от того, редактируется ли пользователь."""
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


# Удаляем стандартный UserAdmin, если он зарегистрирован
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Регистрируем кастомную модель пользователя
admin.site.register(User, CustomUserAdmin)
