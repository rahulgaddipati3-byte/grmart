# orders/views.py
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from store.models import Product
from .models import Order, OrderItem

# We use the same session key as your cart app
CART_SESSION_KEY = "cart"


def _get_cart(session) -> dict:
    cart = session.get(CART_SESSION_KEY)
    if not isinstance(cart, dict):
        cart = {}
        session[CART_SESSION_KEY] = cart
    return cart


def _clear_cart(session) -> None:
    session.pop(CART_SESSION_KEY, None)
    session.modified = True


def _build_cart_items(session):
    """
    Turn the session cart into a list of rows + grand total.
    Each row: {"product", "qty", "price", "line_total"}
    """
    cart = _get_cart(session)
    items = []
    grand_total = Decimal("0")

    for pid, item in cart.items():
        product = get_object_or_404(Product, pk=int(pid))
        price = Decimal(str(item["price"]))
        qty = int(item["qty"])
        line_total = price * qty
        grand_total += line_total

        items.append(
            {
                "product": product,
                "qty": qty,
                "price": price,
                "line_total": line_total,
            }
        )

    return items, grand_total


@login_required
def checkout(request):
    items, grand_total = _build_cart_items(request.session)

    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect("cart:cart_view")

    if request.method == "POST":
        # --- shipping fields from form ---
        full_name = request.POST.get("full_name", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        postal_code = request.POST.get("postal_code", "").strip()
        phone = request.POST.get("phone", "").strip()

        # minimal validation
        if not full_name or not address:
            messages.error(
                request, "Please fill in at least your full name and address."
            )
            return render(
                request,
                "orders/checkout.html",
                {
                    "items": items,
                    "grand_total": grand_total,
                    "full_name": full_name,
                    "address": address,
                    "city": city,
                    "state": state,
                    "postal_code": postal_code,
                    "phone": phone,
                },
            )

        # Build kwargs for Order.create() only using fields that actually exist
        field_names = {f.name for f in Order._meta.get_fields()}
        order_data = {"user": request.user}

        if "total_amount" in field_names:
            order_data["total_amount"] = grand_total

        if "full_name" in field_names:
            order_data["full_name"] = full_name
        if "address" in field_names:
            order_data["address"] = address
        if "city" in field_names:
            order_data["city"] = city
        if "state" in field_names:
            order_data["state"] = state
        if "postal_code" in field_names:
            order_data["postal_code"] = postal_code
        if "phone" in field_names:
            order_data["phone"] = phone
        if "email" in field_names:
            order_data["email"] = request.user.email or ""

        # --- create Order + OrderItems ---
        with transaction.atomic():
            order = Order.objects.create(**order_data)

            for row in items:
                OrderItem.objects.create(
                    order=order,
                    product=row["product"],
                    price=row["price"],
                    qty=row["qty"],
                )

        # clear cart
        _clear_cart(request.session)

        # --- confirmation email (best-effort only) ---
        if request.user.email:
            subject = f"G.R Mart • Order #{order.id} confirmed"
            message = (
                f"Hi {request.user.username},\n\n"
                f"Thank you for shopping with G.R Mart!\n"
                f"Your order #{order.id} has been placed successfully.\n\n"
                "We'll notify you when it ships.\n\n"
                "- G.R Mart team"
            )
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                )
            except Exception:
                # don't break checkout if email fails
                pass

        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect("orders:order_success", order_id=order.id)

    # GET – show checkout form + summary
    return render(
        request,
        "orders/checkout.html",
        {
            "items": items,
            "grand_total": grand_total,
        },
    )


@login_required
def order_success(request, order_id: int):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    return render(
        request,
        "orders/order_success.html",
        {
            "order": order,
            "items": items,
        },
    )


@login_required
def order_history(request):
    """
    Simple "My Orders" page.
    We don't rely on specific field names for created/total.
    """
    orders = Order.objects.filter(user=request.user).order_by("-id")

    for o in orders:
        # pick a created date field if available
        created = None
        for field in ("created_at", "created", "ordered_at", "created_on", "date"):
            if hasattr(o, field):
                created = getattr(o, field)
                break
        o.display_created = created

        # pick a total field (we know you have total_amount from earlier)
        total = getattr(o, "total_amount", None)
        if total is None:
            for fname in ("total", "grand_total", "total_price"):
                if hasattr(o, fname):
                    total = getattr(o, fname)
                    break
        o.display_total = total

    return render(request, "orders/order_history.html", {"orders": orders})
