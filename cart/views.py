# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from store.models import Product

CART_SESSION_KEY = "cart"  # { product_id: {"qty": int, "price": Decimal, "name": str} }

def _get_cart(request):
    cart = request.session.get(CART_SESSION_KEY, {})
    if not isinstance(cart, dict):
        cart = {}
    return cart

def _save_cart(request, cart):
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        qty = int(request.POST.get("qty", "1"))
    except ValueError:
        qty = 1
    qty = max(1, qty)

    # stock guard (optional if you track stock)
    if getattr(product, "stock", None) is not None:
        if qty > product.stock:
            messages.error(request, "Requested quantity exceeds available stock.")
            return redirect("store:product_list")

    cart = _get_cart(request)
    key = str(product.id)
    if key in cart:
        cart[key]["qty"] += qty
    else:
        cart[key] = {
            "qty": qty,
            "price": float(product.price),  # safe for session JSON
            "name": product.name,
            "image": product.image_url if getattr(product, "image_url", None) else "",
        }
    _save_cart(request, cart)
    messages.success(request, f"Added {qty} × {product.name} to cart.")
    return redirect("cart:detail")

def remove_from_cart(request, product_id):
    cart = _get_cart(request)
    key = str(product_id)
    if key in cart:
        del cart[key]
        _save_cart(request, cart)
        messages.info(request, "Item removed from cart.")
    return redirect("cart:detail")

def clear_cart(request):
    _save_cart(request, {})
    messages.info(request, "Cart cleared.")
    return redirect("cart:detail")

def cart_detail(request):
    cart = _get_cart(request)
    items = []
    subtotal = 0.0
    for pid, row in cart.items():
        total = row["qty"] * row["price"]
        subtotal += total
        items.append({
            "id": int(pid),
            "name": row["name"],
            "qty": row["qty"],
            "price": row["price"],
            "total": total,
            "image": row.get("image") or "",
        })
    ctx = {"items": items, "subtotal": subtotal}
    return render(request, "cart/cart_detail.html", ctx)
