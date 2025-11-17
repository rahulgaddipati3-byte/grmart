from django.db import migrations


def seed_products(apps, schema_editor):
    """
    No-op migration to avoid NameError on ITEMS.
    If you want to auto-seed products later,
    you can add Product.objects.create(...) logic here.
    """
    # Example if you want to add items later:
    # Product = apps.get_model("store", "Product")
    # items = [
    #     ("Some Product", 999, 10, "https://example.com/img1.jpg"),
    # ]
    # for name, price, stock, image_url in items:
    #     Product.objects.update_or_create(
    #         name=name,
    #         defaults={
    #             "price": price,
    #             "stock": stock,
    #             "image_url": image_url,
    #         },
    #     )
    pass


def unseed_products(apps, schema_editor):
    """
    Reverse operation for seed_products.
    Currently also a no-op.
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0013_alter_image_url_length"),
    ]

    operations = [
        migrations.RunPython(seed_products, unseed_products),
    ]
