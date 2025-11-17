from django.db import migrations

# (name, price, stock, image_url)
ITEMS = [
    ("Sony Play Station", 49889.00, 50, "https://..."),
    ("Iphone 16 pro", 800000.00, 80, "https://..."),
    ("Oneplus 12", 56299.00, 25, "https://..."),
    ("Apple Macbook Air", 126789.00, 60, "https://..."),
    ("Apple Watch", 39999.00, 100, "https://..."),
    ("Samsung Galaxy S25", 124799.00, 40, "https://..."),
]


def seed_products(apps, schema_editor):
    Product = apps.get_model("store", "Product")

    for name, price, stock, image_url in ITEMS:
        Product.objects.update_or_create(
            name=name,
            defaults={
                "price": price,
                "stock": stock,
                "image_url": image_url,
            },
        )


def unseed_products(apps, schema_editor):
    Product = apps.get_model("store", "Product")
    names = [name for (name, _, _, _) in ITEMS]
    Product.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0013_alter_image_url_length"),
    ]

    operations = [
        migrations.RunPython(seed_products, unseed_products),
    ]
