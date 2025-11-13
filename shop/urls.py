# shop/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Store (must expose a named 'product_list' view inside store/urls.py)
    path("", include(("store.urls", "store"), namespace="store")),

    # Cart (needs app_name = "cart" in cart/urls.py)
    path("cart/", include(("cart.urls", "cart"), namespace="cart")),

    # Accounts (needs app_name = "accounts" in accounts/urls.py)
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
]

# Serve media in dev/Render
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
