# Generated by Django 3.1.7 on 2021-12-01 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0047_auto_20211201_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notam_trafico_charly_new',
            name='es_pib',
            field=models.BooleanField(default=True),
        ),
    ]
