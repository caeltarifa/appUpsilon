# Generated by Django 3.1.1 on 2020-12-04 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0073_auto_20201204_0851'),
    ]

    operations = [
        migrations.RenameField(
            model_name='letra_asunto',
            old_name='descripcion_letra',
            new_name='titulo_letra',
        ),
    ]
