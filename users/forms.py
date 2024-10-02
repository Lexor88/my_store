from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


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
