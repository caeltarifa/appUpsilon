# Generated by Django 3.1.1 on 2020-09-24 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_vuelo', '0024_auto_20200920_0606'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aeropuerto',
            fields=[
                ('aeropuerto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('iata', models.CharField(max_length=5)),
                ('icao', models.CharField(max_length=4)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
            ],
            options={
                'ordering': ['aeropuerto'],
            },
        ),
    ]