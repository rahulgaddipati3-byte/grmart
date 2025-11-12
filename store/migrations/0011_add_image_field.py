from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_product_options'),   # this matches your last valid migration
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='products/', blank=True, null=True),
        ),
    ]

