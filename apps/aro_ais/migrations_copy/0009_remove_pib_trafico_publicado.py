# Generated by Django 3.1.1 on 2020-09-27 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0008_pib_trafico_publicado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pib_trafico',
            name='publicado',
        ),
    ]
