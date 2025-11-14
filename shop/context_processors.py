# cart/context_processors.py
from .views import _get_cart, CART_SESSION_KEY


def cart_count(request):
    """
    Make the cart item count available as `cart_count` in all templates.
    """
    # Pass the *session* into _get_cart, not the request object itself
    cart = _get_cart(request.session)

    # cart is a dict: {"product_id": quantity, ...}
    total_items = sum(cart.values())

    return {"cart_count": total_items}
