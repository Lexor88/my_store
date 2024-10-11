from django import forms
from .models import Mailing, Message, Client


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_date", "periodicity", "status", "message", "clients"]
        widgets = {
            "start_date": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "periodicity": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "message": forms.Select(attrs={"class": "form-control"}),
            "clients": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if not message:
            raise forms.ValidationError("Поле 'Сообщение' не может быть пустым.")
        return message

    def clean_clients(self):
        clients = self.cleaned_data.get("clients")
        if not clients:
            raise forms.ValidationError("Необходимо выбрать хотя бы одного клиента для рассылки.")
        return clients


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["email", "name", "comment"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите email"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите имя"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "placeholder": "Добавьте комментарий"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Client.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email
