# Generated by Django 3.1.1 on 2020-10-11 23:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0028_auto_20201011_1536'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pib_trafico',
            old_name='estacion',
            new_name='instalacion',
        ),
    ]
