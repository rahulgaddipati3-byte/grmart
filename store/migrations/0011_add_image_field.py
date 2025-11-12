# store/migrations/0011_add_image_field.py
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ("store", "0010_alter_product_options"),
    ]

    # No operations: the image column already exists from 0002
    operations = []
