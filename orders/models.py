from django.conf import settings
from django.db import models
from store.models import Product

User = settings.AUTH_USER_MODEL

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255, default="")
    email = models.EmailField(default="")
    phone = models.CharField(max_length=20, default="")

    address1 = models.CharField(max_length=255, default="", blank=True)
    address2 = models.CharField(max_length=255, default="", blank=True)
    city     = models.CharField(max_length=100, default="", blank=True)
    state    = models.CharField(max_length=100, default="", blank=True)
    postcode = models.CharField(max_length=20,  default="", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order   = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty     = models.PositiveIntegerField(default=1)
    price   = models.DecimalField(max_digits=12, decimal_places=2)  # unit price at order time

    def line_total(self):
        return self.qty * self.price

    def __str__(self):
        return f"{self.product} × {self.qty}"
