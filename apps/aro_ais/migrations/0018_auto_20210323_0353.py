# Generated by Django 2.2.5 on 2021-03-23 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0017_delete_banco_notam_charly'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Direccion_amhs',
        ),
        migrations.DeleteModel(
            name='Prioridad',
        ),
        migrations.DeleteModel(
            name='Tipo_notam',
        ),
    ]
