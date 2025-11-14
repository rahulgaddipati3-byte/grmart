# shop/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("store:product_list"), name="home"),
    path("admin/", admin.site.urls),
    path("products/", include(("store.urls", "store"), namespace="store")),
    path("cart/", include(("cart.urls", "cart"), namespace="cart")),
    path("orders/", include(("orders.urls", "orders"), namespace="orders")),
    # ✅ IMPORTANT: namespaced include for accounts
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
]
