# store/urls.py
from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    # Product listing with search
    path("products/", views.product_list, name="product_list"),
]
