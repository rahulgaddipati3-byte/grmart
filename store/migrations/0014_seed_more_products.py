# store/migrations/0014_seed_more_products.py
from django.db import migrations

def seed_products(apps, schema_editor):
    Product = apps.get_model("store", "Product")
    items = [
        ("Sony Play Station ", 49889.00, 50, "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcSz_TLFvvvTE8I4NTNLoxbnOlHBW61qNGLr92vWfYrwg-riGo0SiTcXaU4onAVF5XAoshL8R77XliY9x2XDMP2k8fKuODQGrCYS5-b6nEams18zNKj-ma14uj4DexdRbb3wYQXuPxA&usqp=CAc"),
        ("Iphone 16 pro", 890000.00, 80, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2d3I68z-L4lU7DaXQ76IyA5XkcSoee0kthw&s"),
        ("Oneplus 12", 56299.00, 25, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRENsP3VvhBafIg3OkWYR1xQONvOBhaZ33WMA&s"),
        ("Apple Macbook Air", 126789.00, 60, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMzTx4EXGAsLKYXCkQwrf8pMyUXGWPArDXfQ&s"),
        ("Apple Watch", 39999.00, 100, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRK35c0TiZ8-aixothHxbwutDO3bJkS7LHs9Q&s"),
        ("Samsung Galaxy S25", 124799.00, 40, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKvt0gBzYa7Nn9IQ5JyN611IHGpbRgox5Aaw&s"),
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

