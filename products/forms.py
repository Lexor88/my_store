from django import forms
from .models import Product, BlogPost, Version


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']  # Убедитесь, что поле 'category' нужно или его нужно убрать

    # Список запрещенных слов
    forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        for word in self.forbidden_words:
            if word in name.lower():
                raise forms.ValidationError(f"Название продукта содержит запрещенное слово: {word}")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        for word in self.forbidden_words:
            if word in description.lower():
                raise forms.ValidationError(f"Описание продукта содержит запрещенное слово: {word}")
        return description


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview_image', 'is_published']


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'is_current_version']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})  # Применение класса для всех полей
        self.fields['is_current_version'].widget.attrs.update({'class': 'form-check-input'})  # Для чекбокса

    def clean(self):
        cleaned_data = super().clean()
        # Дополнительная логика валидации, если необходимо
        return cleaned_data
