# store/urls.py
from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),                 # "/" -> welcome page
    path("products/", views.product_list, name="product_list"),  # "/products/"
]
