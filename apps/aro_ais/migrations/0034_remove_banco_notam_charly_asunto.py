# Generated by Django 3.1.7 on 2021-06-18 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0033_notam_trafico_alfa_cancel_notam_trafico_alfa_new_notam_trafico_alfa_repla_notam_trafico_charly_cance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banco_notam_charly',
            name='Asunto',
        ),
    ]
