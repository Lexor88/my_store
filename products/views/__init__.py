# Импорт представлений из отдельных модулей
from .products import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    publish_product,
)
from .blog import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
)
from .versions import (
    VersionCreateView,
    VersionUpdateView,
    VersionDeleteView,
    SetActiveVersionView,
)
from .contact import ContactView

from .category import category_list

# Добавляем пространство имен для приложения 'products'
app_name = "products"
