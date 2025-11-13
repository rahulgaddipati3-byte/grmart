# shop/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


# Fallback for old `{% url 'detail' %}` links in templates
def fallback_detail(request, pk=None):
    """
    Simple temporary view so that any `{% url 'detail' ... %}` calls
    don't crash the site. It just sends the user back to the product list.
    """
    return redirect("store:product_list")


urlpatterns = [
    # Home → products
    path("", RedirectView.as_view(pattern_name="store:product_list", permanent=False), name="home"),

    # 🔴 Fallback route for any old `{% url 'detail' product.id %}` usage
    path("detail/<int:pk>/", fallback_detail, name="detail"),

    path("admin/", admin.site.urls),
    path("products/", include(("store.urls", "store"), namespace="store")),
    path("cart/", include(("cart.urls", "cart"), namespace="cart")),
    path("orders/", include(("orders.urls", "orders"), namespace="orders")),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
