from django.db import migrations

def seed_products(apps, schema_editor):
    Product = apps.get_model("store", "Product")

    items = [
        {
            "name": "Sony PlayStation 5",
            "price": 49990.00,
            "stock": 50,
            "image_url": "https://images.unsplash.com/photo-1606813907291-76b79343e259?q=80&w=1200&auto=format&fit=crop",
        },
        {
            "name": "iPhone 16 Pro",
            "price": 129900.00,
            "stock": 80,
            "image_url": "https://images.unsplash.com/photo-1695048133104-2e0b7c1fba4e?q=80&w=1200&auto=format&fit=crop",
        },
        {
            "name": "OnePlus 12",
            "price": 65999.00,
            "stock": 60,
            "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?q=80&w=1200&auto=format&fit=crop",
        },
        {
            "name": "Apple MacBook Air",
            "price": 99990.00,
            "stock": 40,
            "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?q=80&w=1200&auto=format&fit=crop",
        },
        {
            "name": "Apple Watch",
            "price": 41990.00,
            "stock": 100,
            "image_url": "https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b?q=80&w=1200&auto=format&fit=crop",
        },
        {
            "name": "Samsung Galaxy S25",
            "price": 124999.00,
            "stock": 70,
            "image_url": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?q=80&w=1200&auto=format&fit=crop",
        },
    ]

    for it in items:
        Product.objects.update_or_create(
            name=it["name"],
            defaults={
                "price": it["price"],
                "stock": it["stock"],
                "image_url": it["image_url"],
            },
        )

def unseed_products(apps, schema_editor):
    Product = apps.get_model("store", "Product")
    names = [
        "Sony PlayStation 5",
        "iPhone 16 Pro",
        "OnePlus 12",
        "Apple MacBook Air",
        "Apple Watch",
        "Samsung Galaxy S25",
    ]
    Product.objects.filter(name__in=names).delete()

class Migration(migrations.Migration):
    # make sure this matches your latest schema migration filename
    dependencies = [
    ('store', '0014_seed_more_products'),
]


    operations = [
        migrations.RunPython(seed_products, unseed_products),
    ]

