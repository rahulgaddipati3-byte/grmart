# store/admin.py
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "created_at")
    search_fields = ("name", "description")   # required for autocomplete to work well
    list_filter = ("created_at",)
    ordering = ("-created_at",)
