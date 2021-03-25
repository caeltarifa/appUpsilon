# Generated by Django 3.1.5 on 2021-03-01 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan_vuelo', '0004_auto_20210301_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notam_trafico_alfa_new',
            name='cancel',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='plan_vuelo.notam_trafico_alfa_cancel'),
        ),
        migrations.AlterField(
            model_name='notam_trafico_alfa_new',
            name='replace',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='plan_vuelo.notam_trafico_alfa_repla'),
        ),
        migrations.AlterField(
            model_name='notam_trafico_charly_new',
            name='cancel',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='plan_vuelo.notam_trafico_charly_cancel'),
        ),
        migrations.AlterField(
            model_name='notam_trafico_charly_new',
            name='replace',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='plan_vuelo.notam_trafico_charly_repla'),
        ),
    ]
