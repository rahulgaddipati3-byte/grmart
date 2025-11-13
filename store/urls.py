# store/urls.py
from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    # product list (main page)
    path("", views.product_list, name="product_list"),

    # 🔴 Fallback product detail URL – fixes "Reverse for 'detail'" error
    path("detail/<int:pk>/", views.product_detail_fallback, name="detail"),

    # (keep any other store URLs you already had here)
    # e.g. category filters, etc...
]
