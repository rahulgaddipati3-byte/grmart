from django.db import models

class HomepageContent(models.Model):
    # store a full URL (CDN, S3, or any HTTP image)
    hero_image_url = models.URLField(blank=True, help_text="Full URL to the homepage hero image")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Homepage Content"
