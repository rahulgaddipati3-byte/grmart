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
    if cart is None or not isinstance(cart, dict):
        cart = {}
        session[CART_SESSION_KEY] = cart
    return cart


def add_to_cart(request, product_id):
    """
    Add one unit of the given product to the cart,
    then redirect to the cart detail page.
    """
    product = get_object_or_404(Product, pk=product_id)

    cart = _get_cart(request.session)
    pid = str(product.id)

    cart[pid] = cart.get(pid, 0) + 1
    request.session.modified = True

    return redirect("cart:cart_detail")


def remove_from_cart(request, product_id):
    """
    Remove the product entirely from the cart.
    """
    cart = _get_cart(request.session)
    pid = str(product_id)

    if pid in cart:
        del cart[pid]
        request.session.modified = True

    return redirect("cart:cart_detail")


def cart_detail(request):
    """
    Show all items currently in the cart.
    """
    cart = _get_cart(request.session)
    product_ids = list(cart.keys())

    products = Product.objects.filter(id__in=product_ids)

    items = []
    total = 0

    for product in products:
        pid = str(product.id)
        qty = cart.get(pid, 0)
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
