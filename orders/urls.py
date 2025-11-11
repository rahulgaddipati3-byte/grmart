from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("success/",  views.order_success, name="success"),
    path("checkout/", views.checkout, name="checkout"),
    path("history/", views.order_history, name="order_history"),
    # Success page AFTER placing order
    path("success/<int:order_id>/", views.order_success, name="order_success"),
]
