# Generated by Django 3.1.1 on 2020-10-06 01:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plan_vuelo', '0031_remove_cargo_cuenta_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='cuenta_usuario',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
