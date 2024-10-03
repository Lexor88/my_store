from django.shortcuts import render
from products.services import get_categories


# Список категорий
def category_list(request):
    categories = get_categories()
    return render(request, "products/category_list.html", {"categories": categories})
