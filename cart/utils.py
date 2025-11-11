from decimal import Decimal

SESSION_KEY = "cart"

def _normalize_cart(raw):
    """
    Accepts whatever is in session (dict / list / int / None) and returns
    a clean dict: {product_id(str): qty(int >=1)}.
    """
    normalized = {}

    if raw is None:
        return normalized

    # If someone stored a single int by accident, just ignore it.
    if isinstance(raw, int):
        return normalized

    # Expected shape is a dict {pid: qty}
    if isinstance(raw, dict):
        for k, v in raw.items():
            try:
                pid = str(int(k))
                qty = int(v) if v is not None else 0
            except (ValueError, TypeError):
                continue
            if qty > 0:
                normalized[pid] = normalized.get(pid, 0) + qty
        return normalized

    # Sometimes people store a list of ints or dicts — fold them in.
    if isinstance(raw, list):
        for itm in raw:
            # list of product ids
            if isinstance(itm, int):
                pid = str(itm)
                normalized[pid] = normalized.get(pid, 0) + 1
            # list of dicts like {"product_id": 12, "qty": 3}
            elif isinstance(itm, dict):
                pid = (
                    itm.get("product_id")
                    or itm.get("id")
                    or itm.get("pk")
                )
                try:
                    pid = str(int(pid))
                    qty = int(itm.get("qty") or itm.get("quantity") or 1)
                except (ValueError, TypeError):
                    continue
                if qty > 0:
                    normalized[pid] = normalized.get(pid, 0) + qty
        return normalized

    # Anything else -> empty
    return normalized


def get_cart(request):
    """
    Returns the normalized cart dict stored in session under SESSION_KEY.
    """
    raw = request.session.get(SESSION_KEY)
    cart = _normalize_cart(raw)
    # If normalization changed the shape, persist it.
    if cart != raw:
        request.session[SESSION_KEY] = cart
        request.session.modified = True
    return cart


def get_cart_and_total(request):
    """
    Returns (items, total) where items is a list of:
        {"product": Product, "qty": int, "price": Decimal, "line_total": Decimal}
    and total is a Decimal.
    """
    from store.models import Product  # lazy import to avoid any circulars

    cart = get_cart(request)
    items = []
    total = Decimal("0")

    if not cart:
        return items, total

    # Fetch products in one go
    pids = []
    for pid in cart.keys():
        try:
            pids.append(int(pid))
        except (TypeError, ValueError):
            continue

    products = {p.id: p for p in Product.objects.filter(id__in=pids)}

    for pid_str, qty in cart.items():
        try:
            pid = int(pid_str)
            qty = int(qty)
        except (TypeError, ValueError):
            continue
        if qty <= 0:
            continue

        p = products.get(pid)
        if not p:
            continue

        price = Decimal(p.price or 0)
        line_total = price * qty
        items.append({
            "product": p,
            "qty": qty,
            "price": price,
            "line_total": line_total,
        })
        total += line_total

    return items, total


def clear_cart(request):
    """Remove the cart from session."""
    request.session[SESSION_KEY] = {}
    request.session.modified = True
from decimal import Decimal
from store.models import Product  # safe import here if you prefer

SESSION_KEY = "cart"

def _normalize_cart(raw):
    normalized = {}
    if raw is None: return normalized
    if isinstance(raw, int): return normalized
    if isinstance(raw, dict):
        for k, v in raw.items():
            try:
                pid = str(int(k))
                qty = int(v) if v is not None else 0
            except (ValueError, TypeError):
                continue
            if qty > 0:
                normalized[pid] = normalized.get(pid, 0) + qty
        return normalized
    if isinstance(raw, list):
        for itm in raw:
            if isinstance(itm, int):
                pid = str(itm)
                normalized[pid] = normalized.get(pid, 0) + 1
            elif isinstance(itm, dict):
                pid = itm.get("product_id") or itm.get("id") or itm.get("pk")
                try:
                    pid = str(int(pid))
                    qty = int(itm.get("qty") or itm.get("quantity") or 1)
                except (ValueError, TypeError):
                    continue
                if qty > 0:
                    normalized[pid] = normalized.get(pid, 0) + qty
        return normalized
    return normalized

def get_cart(request):
    raw = request.session.get(SESSION_KEY)
    cart = _normalize_cart(raw)
    if cart != raw:
        request.session[SESSION_KEY] = cart
        request.session.modified = True
    return cart

def save_cart(request, cart):
    request.session[SESSION_KEY] = _normalize_cart(cart)
    request.session.modified = True

def add_item(request, product_id, qty=1, replace=False):
    cart = get_cart(request)
    pid = str(int(product_id))
    if replace:
        cart[pid] = max(0, int(qty))
    else:
        cart[pid] = max(0, int(cart.get(pid, 0)) + int(qty))
    if cart.get(pid, 0) <= 0:
        cart.pop(pid, None)
    save_cart(request, cart)

def remove_item(request, product_id):
    cart = get_cart(request)
    cart.pop(str(int(product_id)), None)
    save_cart(request, cart)

def clear_cart(request):
    request.session[SESSION_KEY] = {}
    request.session.modified = True

def get_cart_and_total(request):
    cart = get_cart(request)
    items, total = [], Decimal("0")
    if not cart:
        return items, total
    pids = [int(pid) for pid in cart.keys() if str(pid).isdigit()]
    products = {p.id: p for p in Product.objects.filter(id__in=pids)}
    for pid_str, qty in cart.items():
        try:
            pid = int(pid_str); qty = int(qty)
        except (TypeError, ValueError):
            continue
        if qty <= 0: continue
        p = products.get(pid)
        if not p: continue
        price = Decimal(p.price or 0)
        line_total = price * qty
        items.append({"product": p, "qty": qty, "price": price, "line_total": line_total})
        total += line_total
    return items, total
