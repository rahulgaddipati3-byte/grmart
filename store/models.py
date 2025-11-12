# store/models.py  (keep exactly this shape)
from django.db import models
from django.templatetags.static import static

class Product(models.Model):
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)  # file uploads
    image_url = models.URLField(max_length=1000,blank=True, null=True)                        # external links
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def image_src(self):
        if self.image_url:
            return self.image_url
        try:
            if self.image and self.image.storage.exists(self.image.name):
                return self.image.url
        except Exception:
            pass
        return static("img/placeholder-product.png")

    def __str__(self):
        return self.name
