# Generated by Django 3.1.1 on 2020-09-27 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('aro_ais', '0013_auto_20200927_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='MODELNAME',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'MODELNAME',
                'verbose_name_plural': 'MODELNAMEs',
            },
        ),
    ]
