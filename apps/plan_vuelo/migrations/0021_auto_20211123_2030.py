# Generated by Django 3.1.7 on 2021-11-23 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_vuelo', '0020_auto_20211123_1946'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aeropuerto',
            old_name='geo_gpe_dme',
            new_name='dvor_dme',
        ),
        migrations.AddField(
            model_name='aeropuerto',
            name='ils_llz',
            field=models.CharField(blank=True, default='NIL', max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='aeropuerto',
            name='ils_loc',
            field=models.CharField(blank=True, default='NIL', max_length=25, null=True),
        ),
    ]
