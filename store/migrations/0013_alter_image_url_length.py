from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("store", "0012_promote_admin_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image_url",
            field=models.URLField(max_length=3000, blank=True, null=True),
        ),
    ]
