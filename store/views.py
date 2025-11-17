# store/views.py
from django.shortcuts import render
from .models import Product
from django.shortcuts import render, redirect

def home(request):
    """
    Welcome / landing page at "/".
    Uses templates/home.html
    """
    return render(request, "home.html")


def product_list(request):
    """
    Products + Today's Deals page at "/products/".
    Uses templates/store/product_list.html
    """
    # Is this the "Today's Deals" view?
    is_deals = request.GET.get("filter") == "today"

    # Price filter
    price_filter = request.GET.get("price")

    products = Product.objects.all()

    # Optional: if you have an `is_deal` boolean on Product
    if is_deals and hasattr(Product, "is_deal"):
        products = products.filter(is_deal=True)

    if price_filter == "under-1000":
        products = products.filter(price__lt=1000)
    elif price_filter == "1000-10000":
        products = products.filter(price__gte=1000, price__lte=10000)
    elif price_filter == "above-10000":
        products = products.filter(price__gt=10000)

    context = {
        "products": products,
        "is_deals": is_deals,
        "price_filter": price_filter,
    }
    return render(request, "store/product_list.html", context)
def today_deals(request):
    # For now, just reuse product list or some simple page
    return redirect("store:product_list")
    # or: return render(request, "store/today_deals.html"