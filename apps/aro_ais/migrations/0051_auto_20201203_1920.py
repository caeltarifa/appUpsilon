# Generated by Django 3.1.1 on 2020-12-03 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0050_auto_20201203_1919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estado_asunto',
            old_name='id_asunto',
            new_name='asunto',
        ),
    ]
