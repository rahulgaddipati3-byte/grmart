# store/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.shortcuts import render


def product_list(request):
    products = Product.objects.all()
    ctx = {
        "products": products,
    }
    return render(request, "products/product_list.html", ctx)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ctx = {
        "product": product,
    }
    return render(request, "products/product_detail.html", ctx)
def home(request):
    return render(request, "store/home.html")
