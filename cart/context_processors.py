# cart/context_processors.py

from .views import _get_cart


def cart_count(request):
    """
    Expose the total number of items in the cart
    as `cart_count` in all templates.
    """
    cart = _get_cart(request.session)
    total_items = sum(cart.values())
    return {"cart_count": total_items}
