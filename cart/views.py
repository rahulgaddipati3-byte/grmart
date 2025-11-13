from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from store.models import Product

CART_SESSION_KEY = "cart"

def _get_cart(request):
    cart = request.session.get(CART_SESSION_KEY, {})
    # ensure types are ints
    cart = {int(pid): int(qty) for pid, qty in cart.items()}
    request.session[CART_SESSION_KEY] = cart
    return cart

def cart_view(request):
    cart = _get_cart(request)
    items = []
    total = 0
    for pid, qty in cart.items():
        product = get_object_or_404(Product, pk=pid)
        line_total = float(product.price) * qty
        total += line_total
        items.append({"product": product, "qty": qty, "line_total": line_total})
    ctx = {"items": items, "total": total}
    return render(request, "cart/cart_detail.html", ctx)

@require_POST
def add_to_cart(request, product_id):
    cart = _get_cart(request)
    qty = int(request.POST.get("qty", 1))
    product = get_object_or_404(Product, pk=product_id)
    # clamp to stock if stock is tracked
    if product.stock is not None:
        qty = max(1, min(qty, int(product.stock)))
    cart[product_id] = cart.get(product_id, 0) + qty
    request.session.modified = True
    return redirect("cart:view")

def remove_from_cart(request, product_id):
    cart = _get_cart(request)
    if product_id in cart:
        del cart[product_id]
        request.session.modified = True
    return redirect("cart:view")

def clear_cart(request):
    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True
    return redirect("cart:view")
