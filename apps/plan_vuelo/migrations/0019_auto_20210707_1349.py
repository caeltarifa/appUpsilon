# Generated by Django 3.1.7 on 2021-07-07 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_vuelo', '0018_aeropuerto_geo_ndb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aeropuerto',
            name='geo_arp',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='aeropuerto',
            name='geo_gpe_dme',
            field=models.CharField(blank=True, default='NIL', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='aeropuerto',
            name='geo_ils',
            field=models.CharField(blank=True, default='NIL', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='aeropuerto',
            name='geo_ils_gp_dme',
            field=models.CharField(blank=True, default='NIL', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='aeropuerto',
            name='geo_l',
            field=models.CharField(blank=True, default='NIL', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='aeropuerto',
            name='geo_marcador',
            field=models.CharField(blank=True, default='NIL', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='aeropuerto',
            name='geo_ndb',
            field=models.CharField(blank=True, default='NIL', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='aeropuerto',
            name='geo_vor',
            field=models.CharField(blank=True, default='NIL', max_length=25, null=True),
        ),
    ]
