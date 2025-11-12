# store/migrations/0014_seed_more_products.py
from django.db import migrations

def seed_products(apps, schema_editor):
    Product = apps.get_model("store", "Product")
    items = [
        {"name": "iPhone 15", "price": 79900, "stock": 20,
         "image_url": "https://images.unsplash.com/photo-1695047996728-b4-iphone15?w=1200"},
        {"name": "Samsung Galaxy S24", "price": 69900, "stock": 25,
         "image_url": "https://images.unsplash.com/photo-1701000000000-galaxy-s24?w=1200"},
        {"name": "Sony WH-1000XM5", "price": 29990, "stock": 30,
         "image_url": "https://images.unsplash.com/photo-1651000000000-sony-xm5?w=1200"},
        {"name": "Dell XPS 13", "price": 124990, "stock": 10,
         "image_url": "https://images.unsplash.com/photo-1555617117-08d3e5d8d9b7?w=1200"},
        {"name": "Nike Air Max", "price": 9990, "stock": 40,
         "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=1200"},
    ]
    for it in items:
        Product.objects.update_or_create(
            name=it["name"],
            defaults={
                "price": it["price"] / 100 if isinstance(it["price"], int) else it["price"],
                "stock": it["stock"],
                "image_url": it["image_url"],
            },
        )

def unseed_products(apps, schema_editor):
    Product = apps.get_model("store", "Product")
    Product.objects.filter(name__in=[
        "iPhone 15", "Samsung Galaxy S24", "Sony WH-1000XM5", "Dell XPS 13", "Nike Air Max"
    ]).delete()

class Migration(migrations.Migration):
    dependencies = [
        ("store", "0013_alter_image_url_length"),
    ]
    operations = [
        migrations.RunPython(seed_products, reverse_code=unseed_products),
    ]

