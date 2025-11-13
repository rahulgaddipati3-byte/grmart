# cart/urls.py
from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="detail"),
    path("add/", views.add_to_cart, name="add"),
    path("remove/<int:product_id>/", views.remove_item, name="remove"),
    path("clear/", views.clear_cart, name="clear"),
]
