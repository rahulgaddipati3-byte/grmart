# cart/context_processors.py
from .views import _get_cart

def cart_count(request):
    cart = _get_cart(request)
    total_qty = sum(item["quantity"] for item in cart.values())
    return {"cart_count": total_qty}
