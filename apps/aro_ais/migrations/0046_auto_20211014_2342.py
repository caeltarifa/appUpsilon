# Generated by Django 3.1.7 on 2021-10-14 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0045_auto_20210721_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notam_trafico_alfa_new',
            name='asunto',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='notam_trafico_charly_new',
            name='asunto',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='notam_trafico_charly_new',
            name='estado_asunto',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='notam_trafico_charly_new',
            name='pib_publicar',
            field=models.CharField(max_length=1500),
        ),
    ]
