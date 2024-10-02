from .blog import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
)

from .products import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    publish_product,
)

from .versions import (
    VersionCreateView,
    VersionUpdateView,
    VersionDeleteView,
    SetActiveVersionView,
)

from .contact import ContactView  # Добавляем импорт ContactView
