# Generated by Django 3.1.5 on 2021-03-17 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0008_historico_pib'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historico_pib',
            name='lista_notam',
            field=models.CharField(max_length=800),
        ),
    ]
