# orders/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from store.models import Product
from .models import Order, OrderItem


def _build_cart_items(request):
    """
    Read the cart from the session and return:
      - cart_items: list of dicts with product, quantity, price, subtotal
      - total_amount: sum of all subtotals
    Session cart format: { "product_id": quantity, ... }
    """
    cart = request.session.get("cart", {})

    cart_items = []
    total_amount = 0

    for product_id_str, qty in cart.items():
        product = get_object_or_404(Product, pk=int(product_id_str))
        qty = int(qty)

        subtotal = product.price * qty
        cart_items.append(
            {
                "product": product,
                "quantity": qty,
                "price": product.price,
                "subtotal": subtotal,
            }
        )
        total_amount += subtotal

    return cart_items, total_amount


@login_required
def checkout(request):
    cart_items, total_amount = _build_cart_items(request)

    # If cart is empty, go back to cart page
    if not cart_items:
        return redirect("cart:view")

    if request.method == "POST":
        # ❌ DO NOT pass total_amount here (field doesn't exist on model)
        order = Order.objects.create(
            user=request.user,
            # add other required fields here if your Order model needs them
            # e.g. first_name=..., address=..., etc.
        )

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["price"],
                # if you have a subtotal field, you can add it too:
                # subtotal=item["subtotal"],
            )

        # Clear cart
        request.session["cart"] = {}
        request.session.modified = True

        # Redirect to success page for this order
        return redirect("orders:success", order_id=order.id)

    # GET → show checkout page
    context = {
        "cart_items": cart_items,
        "total_amount": total_amount,
    }
    return render(request, "orders/checkout.html", context)


@login_required
def success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    # Calculate total based on OrderItems instead of a field on Order
    items = order.items.all()  # related_name='items' in OrderItem(order=...)
    total_amount = sum(item.price * item.quantity for item in items)

    context = {
        "order": order,
        "items": items,
        "total_amount": total_amount,
    }
    return render(request, "orders/success.html", context)
