from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # 👉 All store URLs (home, products, etc) live at the site root
    path("", include(("store.urls", "store"), namespace="store")),

    # Cart & orders keep their own namespaces
    path("cart/", include(("cart.urls", "cart"), namespace="cart")),
    path("orders/", include(("orders.urls", "orders"), namespace="orders")),

    # Accounts
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
]
