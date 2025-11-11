# store/migrations/0008_update_product_images.py
from django.db import migrations


def update_product_images(apps, schema_editor):
    Product = apps.get_model("store", "Product")

    updates = {
        "Nifty Tee": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQL0uyFBbFExnp5rLXLetjqW0_k-1Rk4SdPrQ&s",
        "BankNifty Mug": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5hka79Q8eE0NJ5JEHBcwZ5_4sBt1s4IB5_g&s",
        "Algo Hoodie": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf-PRb0T3R_pn1k9zfa-5haK5fsaaibbpzqg&s",
    }

    for name, url in updates.items():
        try:
            product = Product.objects.get(name=name)
            product.image_url = url
            product.save()
        except Product.DoesNotExist:
            # If the product isn't there (e.g. new DB), just skip
            pass


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0007_rename_remote_image_url_product_image_url"),
        # ^ this must be the LAST store migration that already exists
    ]

    operations = [
        migrations.RunPython(update_product_images),
    ]
