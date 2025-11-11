from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product

CART_SESSION_KEY = "cart"


def _get_cart(session) -> dict:
    """Return a dict cart from session. If corrupted/mis-typed, reset to {}."""
    cart = session.get(CART_SESSION_KEY)
    if not isinstance(cart, dict):
        cart = {}
        session[CART_SESSION_KEY] = cart
    return cart


def _save_cart(session, cart: dict) -> None:
    session[CART_SESSION_KEY] = cart
    session.modified = True


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    cart = _get_cart(request.session)

    # qty from form, default 1
    try:
        qty = int(request.POST.get("qty", 1))
    except (TypeError, ValueError):
        qty = 1
    if qty < 1:
        qty = 1

    pid = str(product.id)
    # item shape in cart
    item = cart.get(pid, {
        "name": product.name,
        "price": str(product.price),  # keep price as string in session
        "qty": 0,
    })
    item["qty"] = int(item.get("qty", 0)) + qty
    cart[pid] = item
    _save_cart(request.session, cart)

    return redirect("cart:cart_view")


@login_required
def cart_view(request):
    cart = _get_cart(request.session)
    items = []
    grand_total = Decimal("0")

    for pid, item in cart.items():
        price = Decimal(item["price"])
        qty = int(item["qty"])
        subtotal = price * qty
        grand_total += subtotal
        items.append({
            "id": int(pid),
            "name": item["name"],
            "price": price,
            "qty": qty,
            "subtotal": subtotal,
        })

    return render(request, "cart/cart_view.html", {
        "items": items,
        "grand_total": grand_total,
    })


@login_required
def update_qty(request, pk):
    cart = _get_cart(request.session)
    pid = str(pk)
    if request.method == "POST" and pid in cart:
        try:
            qty = int(request.POST.get("qty", 1))
        except (TypeError, ValueError):
            qty = 1
        if qty <= 0:
            cart.pop(pid, None)
        else:
            cart[pid]["qty"] = qty
        _save_cart(request.session, cart)
    return redirect("cart:cart_view")


@login_required
def remove_item(request, pk):
    cart = _get_cart(request.session)
    cart.pop(str(pk), None)
    _save_cart(request.session, cart)
    return redirect("cart:cart_view")


@login_required
def clear_cart(request):
    request.session.pop(CART_SESSION_KEY, None)
    request.session.modified = True
    return redirect("cart:cart_view")
