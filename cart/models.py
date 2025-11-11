# cart/models.py
from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Cart(models.Model):
    """
    One row per (user, product) in the cart.
    Quantity is how many units of that product the user added.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="in_carts")
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate rows of the same product for the same user
        unique_together = ("user", "product")
        ordering = ("-added_at",)

    def __str__(self):
        return f"{self.user.username} — {self.product.name} (x{self.quantity})"

    # Used in admin/list displays and templates
    def line_total(self):
        return self.product.price * self.quantity

    # Nice alias if a template expects "total_price"
    @property
    def total_price(self):
        return self.line_total()

