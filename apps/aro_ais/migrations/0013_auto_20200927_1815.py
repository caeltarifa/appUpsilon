# Generated by Django 3.1.1 on 2020-09-27 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0012_pib_extenso'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pib_trafico',
            name='oficialaro',
        ),
        migrations.RemoveField(
            model_name='pib_trafico',
            name='ref_notam_amhs',
        ),
        migrations.DeleteModel(
            name='Pib_extenso',
        ),
        migrations.DeleteModel(
            name='Pib_trafico',
        ),
    ]
