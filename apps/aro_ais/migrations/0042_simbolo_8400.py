# Generated by Django 3.1.1 on 2020-12-01 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0041_auto_20201125_0945'),
    ]

    operations = [
        migrations.CreateModel(
            name='Simbolo_8400',
            fields=[
                ('id_simbolo', models.AutoField(primary_key=True, serialize=False)),
                ('simbolo', models.CharField(max_length=1)),
                ('descripcion', models.CharField(max_length=150)),
            ],
        ),
    ]
