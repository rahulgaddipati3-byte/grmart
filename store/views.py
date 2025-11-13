# store/views.py
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Product


def home(request):
    """Send '/' traffic to the products list."""
    return redirect("product_list")


def product_list(request):
    """
    List products.
    - Supports search via ?q=... (multi-term AND search).
    - Does NOT exclude stock=0; template shows 'Out of stock'.
    """
    query = (request.GET.get("q") or "").strip()
    products = Product.objects.all()

    if query:
        # Allow queries like 'apple iphone' or 'apple+iphone'
        terms = [t for t in query.replace("+", " ").split() if t]
        for t in terms:
            products = products.filter(Q(name__icontains=t))

    products = products.order_by("-created_at", "name")
    ctx = {"products": products, "query": query}
    return render(request, "products/product_list.html", ctx)


def product_detail(request, pk):
    """
    Optional detail view (safe to keep even if not used by URLs).
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})
def product_detail_fallback(request, pk=None):
    """
    Temporary fallback so that any `{% url 'detail' %}` calls
    won't crash the site. Just send users back to the product list.
    """
    return redirect("store:product_list")
