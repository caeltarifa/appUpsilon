# Generated by Django 3.1.5 on 2021-03-19 16:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_vuelo', '0008_auto_20210317_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='flp_trafico',
            name='ingresado',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
