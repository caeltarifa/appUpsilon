# Generated by Django 3.1.1 on 2020-10-12 06:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_vuelo', '0036_flp_aprobado_date_aprobado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flp_aprobado',
            name='date_aprobado',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]