from django.db import migrations

# (name, price, stock, image_url)


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
