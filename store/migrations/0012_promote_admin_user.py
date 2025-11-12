from django.db import migrations
import os
from django.contrib.auth.hashers import make_password

def promote_or_create_admin(apps, schema_editor):
    User = apps.get_model("auth", "User")

    username = os.getenv("DJANGO_ADMIN_USERNAME", "king")
    email    = os.getenv("DJANGO_ADMIN_EMAIL",    "king@example.com")
    password = os.getenv("DJANGO_ADMIN_PASSWORD", "Admin!234")  # change later

    # create or fetch
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email},
    )

    # keep email updated if you like
    user.email = email

    # set flags
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True

    # hash password (can't use set_password in migrations)
    user.password = make_password(password)

    user.save()

def noop_reverse(apps, schema_editor):
    # no rollback (we don't demote/delete admin on reverse)
    pass

class Migration(migrations.Migration):

    dependencies = [
        ("store", "0011_add_image_field"),
    ]

    operations = [
        migrations.RunPython(promote_or_create_admin, noop_reverse),
    ]
