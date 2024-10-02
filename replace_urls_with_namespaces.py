import os
import re

# Укажите путь к вашей директории с шаблонами
templates_dir = "./my_store/templates/"

# Определите регулярное выражение для поиска тега url без пространства имен
url_pattern_products = re.compile(r"{% url '(product_[^']+)'")
url_pattern_users = re.compile(
    r"{% url '(edit_profile|login|register|reset_password|logout)'"
)


# Функция для обработки файлов
def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    # Замените совпадения с добавлением пространства имен 'products' или 'users'
    new_content = url_pattern_products.sub(r"{% url 'products:\1'", content)
    new_content = url_pattern_users.sub(r"{% url 'users:\1'", new_content)

    # Сохраните изменения
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(new_content)


# Проход по файлам в директории шаблонов
for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith(".html"):
            process_file(os.path.join(root, file))

print("Замены завершены.")
