# Generated by Django 3.1.1 on 2020-10-04 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_vuelo', '0027_auto_20200927_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='flp_aprobado',
            name='en_curso',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='flp_aprobado',
            name='finalizado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='flp_aprobado',
            name='por_trabajar',
            field=models.BooleanField(default=True),
        ),
    ]
