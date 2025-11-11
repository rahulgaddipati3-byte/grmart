# store/migrations/0009_fix_banknifty_image.py
from django.db import migrations


def fix_banknifty_image(apps, schema_editor):
    Product = apps.get_model("store", "Product")
    try:
        product = Product.objects.get(name="BankNifty Mug")
        product.image_url = (
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5hka79Q8eE0NJ5JEHBcwZ5_4sBt1s4IB5_g&s"
        )
        product.save()
    except Product.DoesNotExist:
        # If the product isn't there in this DB, just skip
        pass


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0008_update_product_images"),  # last migration you created
    ]

    operations = [
        migrations.RunPython(fix_banknifty_image),
    ]
