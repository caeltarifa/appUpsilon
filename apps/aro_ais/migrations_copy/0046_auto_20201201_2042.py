# Generated by Django 3.1.1 on 2020-12-01 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0045_auto_20201201_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abreviatura_8400',
            name='id',
        ),
        migrations.AlterField(
            model_name='abreviatura_8400',
            name='abreviatura',
            field=models.CharField(max_length=15, primary_key=True, serialize=False),
        ),
    ]