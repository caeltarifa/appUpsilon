# Generated by Django 3.1.1 on 2020-10-10 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0023_auto_20200929_0518'),
    ]

    operations = [
        migrations.AddField(
            model_name='pib_trafico',
            name='estacion',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
