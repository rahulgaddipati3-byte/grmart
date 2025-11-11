# cart/admin.py
from django.contrib import admin
from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity", "added_at", "line_total_display")
    list_display_links = ("id",)
    search_fields = ("user__username", "product__name")
    list_filter = ("added_at", "product")
    autocomplete_fields = ("user", "product")
    ordering = ("-added_at",)

    @admin.display(description="Line Total")
    def line_total_display(self, obj):
        try:
            return obj.line_total()
        except Exception:
            return "-"
