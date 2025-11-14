# shop/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", lambda request: redirect("store:product_list"), name="home"),
    path("products/", include(("store.urls", "store"), namespace="store")),
    path("cart/", include(("cart.urls", "cart"), namespace="cart")),
]
