# Generated by Django 3.1.1 on 2020-12-01 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0042_simbolo_8400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simbolo_8400',
            name='simbolo',
            field=models.CharField(max_length=2),
        ),
    ]
