from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # ✅ THIS WAS MISSING

urlpatterns = [
    # Home → redirect to product list
    path("", lambda request: redirect("store:product_list"), name="home"),

    # Store / products
    path("products/", include(("store.urls", "store"), namespace="store")),

    # Cart
    path("cart/", include(("cart.urls", "cart"), namespace="cart")),

    # Orders
    path("orders/", include(("orders.urls", "orders"), namespace="orders")),

    # Accounts / auth
    path("accounts/", include("accounts.urls")),

    # Admin
    path("admin/", admin.site.urls),
]
