from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import User  # Импортируем вашу кастомную модель пользователя

class UserRegistrationForm(UserCreationForm):
    # Делает поле аватара необязательным
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "email",
            "password1",
            "password2",
            "avatar",
            "phone_number",
            "country",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone_number = self.cleaned_data.get("phone_number")
        user.country = self.cleaned_data.get("country")
        if self.cleaned_data.get("avatar"):
            user.avatar = self.cleaned_data["avatar"]
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Группы'
    )

    class Meta:
        model = User
        fields = ['email', 'groups']  # Укажите только те поля, которые есть в вашей модели User

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Устанавливаем группы
            user.groups.set(self.cleaned_data['groups'])
        return user
