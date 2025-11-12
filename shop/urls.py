# shop/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path("", views.home, name="home"),      
    path("admin/", admin.site.urls),
    path("", include("store.urls")),       # 👈 this includes your store app URLs
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/register/", RedirectView.as_view(pattern_name="signup", permanent=False)),

]

# Serve media (for product images) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
