# cart/urls.py
from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    # /cart/  -> main cart page
    path("", views.cart_view, name="cart_view"),

    # /cart/add/5/  -> add product id 5
    path("add/<int:pk>/", views.add_to_cart, name="add_to_cart"),

    # /cart/update/5/  -> update quantity of product id 5
    path("update/<int:pk>/", views.update_qty, name="update_qty"),

    # /cart/remove/5/  -> remove product id 5 from cart
    path("remove/<int:pk>/", views.remove_item, name="remove_item"),

    # /cart/clear/  -> clear the entire cart
    path("clear/", views.clear_cart, name="clear_cart"),
]
