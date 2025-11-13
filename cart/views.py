# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from store.models import Product

CART_SESSION_KEY = "cart"

def _get_cart(request):
    cart = request.session.get(CART_SESSION_KEY, {})
    if not isinstance(cart, dict):
        cart = {}
    return cart

def _save_cart(request, cart):
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

def cart_detail(request):
    cart = _get_cart(request)
    items, subtotal = [], 0
    for pid_str, qty in cart.items():
        try:
            product = Product.objects.get(pk=int(pid_str))
            qty = int(qty)
            line_total = float(product.price) * qty
            subtotal += line_total
            items.append({
                "product": product,
                "qty": qty,
                "line_total": line_total,
            })
        except Product.DoesNotExist:
            continue
    return render(request, "cart/detail.html", {"items": items, "subtotal": subtotal})

@require_POST
def add_to_cart(request):
    product_id = request.POST.get("product_id")
    qty = request.POST.get("qty", "1")
    product = get_object_or_404(Product, pk=product_id)

    try:
        qty = max(1, int(qty))
    except ValueError:
        qty = 1

    if product.stock is not None and product.stock <= 0:
        messages.warning(request, f"{product.name} is out of stock.")
        return _back_to_products(request)

    cart = _get_cart(request)
    current = int(cart.get(str(product.id), 0))
    new_qty = current + qty

    if product.stock is not None and new_qty > product.stock:
        new_qty = product.stock
        messages.info(request, f"Limited stock. Set quantity of {product.name} to {new_qty}.")

    cart[str(product.id)] = new_qty
    _save_cart(request, cart)
    messages.success(request, f"Added {qty} × {product.name} to cart.")
    return _back_to_products(request)

def remove_item(request, product_id: int):
    cart = _get_cart(request)
    cart.pop(str(product_id), None)
    _save_cart(request, cart)
    messages.info(request, "Removed item from cart.")
    return redirect("cart:detail")

def clear_cart(request):
    _save_cart(request, {})
    messages.info(request, "Cart cleared.")
    return redirect("cart:detail")

def _back_to_products(request):
    # send user back to product list retaining filters/search if present
    ref = request.META.get("HTTP_REFERER")
    return redirect(ref or "store:product_list")
