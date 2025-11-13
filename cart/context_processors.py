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
