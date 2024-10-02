from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


class UserRegistrationForm(UserCreationForm):
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
            raise forms.ValidationError(
                "Пользователь с таким email уже существует."
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_active = (
            False  # Делаем пользователя неактивным до подтверждения email
        )

        if commit:
            user.save()

        return user

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = reverse(
            "users:verify_email", kwargs={"uidb64": uid, "token": token}
        )
        full_url = f"{settings.SITE_URL}{verification_url}"

        subject = "Подтверждение вашей электронной почты"
        message = f"Пожалуйста, подтвердите свою электронную почту, перейдя по ссылке: {full_url}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


class CustomUserChangeForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Группы",
    )

    class Meta:
        model = User
        fields = ["email", "groups"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Устанавливаем группы
            user.groups.set(self.cleaned_data["groups"])
        return user
