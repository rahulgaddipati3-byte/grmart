# shop/context_processors.py
def cart_context(request):
    # example values — adapt to your project
    cart = request.session.get("cart", {})
    item_count = sum(item.get("qty", 0) for item in cart.values())
    return {
        "cart_item_count": item_count,
    }
