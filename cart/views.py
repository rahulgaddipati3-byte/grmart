# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product

CART_SESSION_KEY = "cart"


def _get_cart(session):
    """
    Get the cart dict from the session.

    Shape: {"product_id": quantity, ...}
    """
    cart = session.get(CART_SESSION_KEY)
    if cart is None:
        cart = {}
        session[CART_SESSION_KEY] = cart
    return cart


def add_to_cart(request, product_id):
    """
    Add a product to the session cart.
    """
    product = get_object_or_404(Product, pk=product_id)

    cart = _get_cart(request.session)
    qty = int(request.POST.get("quantity", 1))
    if qty < 1:
        qty = 1

    cart[str(product_id)] = cart.get(str(product_id), 0) + qty
    request.session.modified = True

    # After adding, go to cart page
    return redirect("cart:detail")


def remove_item(request, product_id):
    """
    Remove a single product from the session cart.
    """
    cart = _get_cart(request.session)
    cart.pop(str(product_id), None)
    request.session.modified = True
    return redirect("cart:detail")


def clear_cart(request):
    """
    Clear all items from the cart.
    """
    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True
    return redirect("cart:detail")


def cart_detail(request):
    """
    Show all items in the cart.
    """
    cart = _get_cart(request.session)

    items = []
    total = 0

    for product_id, qty in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        line_total = product.price * qty
        total += line_total

        items.append(
            {
                "product": product,
                "quantity": qty,
                "line_total": line_total,
            }
        )

    context = {
        "cart_items": items,
        "cart_total": total,
    }
    return render(request, "cart/cart_detail.html", context)
