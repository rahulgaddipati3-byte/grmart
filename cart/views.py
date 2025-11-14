from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product

# Key used to store the cart in the session
CART_SESSION_KEY = "cart"


def _get_cart(request):
    """
    Internal helper to fetch the cart from the session.
    Always expects a *request* object (not request.session).
    If it doesn't exist yet, create an empty one.
    """
    session = request.session
    cart = session.get(CART_SESSION_KEY)
    if cart is None:
        cart = {}
        session[CART_SESSION_KEY] = cart
    # Mark the session modified so Django will save it
    session.modified = True
    return cart


def _save_cart(request, cart):
    """Save the updated cart back into the session."""
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True


def cart_detail(request):
    """
    Show the contents of the cart.
    Template: cart/cart_detail.html
    Context:
        cart_items: list of { product, quantity, subtotal }
        cart_total: total value
    """
    cart = _get_cart(request)

    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )
        total += subtotal

    context = {
        "cart_items": items,
        "cart_total": total,
    }
    return render(request, "cart/cart_detail.html", context)


def add_to_cart(request, product_id):
    """
    Add one unit of the product to the cart.
    Then redirect to the cart detail page.
    """
    cart = _get_cart(request)
    pid = str(product_id)

    cart[pid] = cart.get(pid, 0) + 1
    _save_cart(request, cart)

    return redirect("cart:detail")


def remove_from_cart(request, product_id):
    """
    Remove a product completely from the cart.
    Then redirect back to the cart page.
    """
    cart = _get_cart(request)
    pid = str(product_id)

    if pid in cart:
        del cart[pid]
        _save_cart(request, cart)

    return redirect("cart:detail")


def clear_cart(request):
    """
    Clear the entire cart from the session,
    then redirect to the (now empty) cart page.
    """
    if CART_SESSION_KEY in request.session:
        del request.session[CART_SESSION_KEY]
        request.session.modified = True

    return redirect("cart:detail")
