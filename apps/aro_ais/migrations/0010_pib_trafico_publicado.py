# Generated by Django 3.1.1 on 2020-09-27 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0009_remove_pib_trafico_publicado'),
    ]

    operations = [
        migrations.AddField(
            model_name='pib_trafico',
            name='publicado',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
