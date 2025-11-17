from django.urls import path
from . import views

app_name = "cart"  # ✅ namespace used as 'cart:...'

urlpatterns = [
    # Cart main page – this is what {% url 'cart:detail' %} should point to
    path("", views.cart_detail, name="detail"),

    # Add item to cart
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),

    # Remove a single product from cart
    path("remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),

    # Clear entire cart
    path("clear/", views.clear_cart, name="clear_cart"),
    path("", views.cart_detail, name="cart_detail"),
]
