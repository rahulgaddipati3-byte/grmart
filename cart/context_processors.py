from .views import _get_cart


def cart_count(request):
    """
    Adds `cart_count` (total quantity of all items) to the template context.
    Used in base.html / navbar.
    """
    cart = _get_cart(request)  # IMPORTANT: pass *request*, not request.session
    total_quantity = sum(cart.values())
    return {"cart_count": total_quantity}
