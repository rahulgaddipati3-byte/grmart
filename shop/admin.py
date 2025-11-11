from django.contrib import admin
from .models import HomepageContent

@admin.register(HomepageContent)
class HomepageContentAdmin(admin.ModelAdmin):
    list_display = ("id", "hero_image_url", "updated_at")
