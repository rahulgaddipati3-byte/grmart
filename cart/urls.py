# cart/urls.py
from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    # Cart detail page  ->  /cart/
    path("", views.cart_detail, name="detail"),

    # Add a product to cart  ->  /cart/add/1/
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),

    # Remove a single product from cart  ->  /cart/remove/1/
    path("remove/<int:product_id>/", views.remove_item, name="remove_item"),

    # Clear the whole cart  ->  /cart/clear/
    path("clear/", views.clear_cart, name="clear_cart"),
]
