# store/views.py
from django.shortcuts import render
from django.db.models import Q
from .models import Product


def product_list(request):
    products = Product.objects.all()

    q = request.GET.get("q", "").strip()
    if q:
        # Filter only on fields that actually exist: here, just name
        products = products.filter(
            Q(name__icontains=q)
        )

    # Debug line – optional, remove later
    print("DEBUG product count:", products.count())

    return render(request, "store/product_list.html", {
        "products": products,
    })
