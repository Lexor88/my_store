from django import forms
from .models import Product, BlogPost, Version


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "image"]

    # Список запрещенных слов
    forbidden_words = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "form-control"}
            )  # Добавляем класс для всех полей

    def save(self, commit=True):
        product = super().save(commit=False)
        product.owner = self.user
        if commit:
            product.save()
        return product

    def clean_name(self):
        name = self.cleaned_data.get("name")
        self.validate_forbidden_words(name, "названии продукта")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        self.validate_forbidden_words(description, "описании продукта")
        return description

    def validate_forbidden_words(self, text, field_name):
        for word in self.forbidden_words:
            if word in text.lower():
                raise forms.ValidationError(
                    f"{field_name.capitalize()} содержит запрещенное слово: {word}"
                )

    def clean_slug(self):
        slug = slugify(self.cleaned_data["name"])
        if Product.objects.filter(slug=slug).exists():
            raise forms.ValidationError("Слаг должен быть уникальным.")
        return slug


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content", "preview_image", "is_published"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "form-control"}
            )  # Добавляем класс для всех полей

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 5:
            raise forms.ValidationError(
                "Заголовок должен содержать минимум 5 символов."
            )
        return title

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) < 20:
            raise forms.ValidationError(
                "Контент должен содержать минимум 20 символов."
            )
        return content


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = [
            "product",
            "version_number",
            "version_name",
            "is_current_version",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
        self.fields["is_current_version"].widget.attrs.update(
            {"class": "form-check-input"}
        )

    def clean_version_number(self):
        version_number = self.cleaned_data.get("version_number")
        if not version_number:
            raise forms.ValidationError("Номер версии не может быть пустым.")
        return version_number

    def clean(self):
        cleaned_data = super().clean()
        is_current = cleaned_data.get("is_current_version")
        product = cleaned_data.get("product")

        if (
            is_current
            and Version.objects.filter(
                product=product, is_current_version=True
            )
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError(
                "У этого продукта уже есть текущая версия."
            )
        return cleaned_data
