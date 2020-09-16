# Generated by Django 3.1.1 on 2020-09-13 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan_vuelo', '0013_auto_20200913_0402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flp_aprobado',
            name='id_flpaprobado',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='xxxx', serialize=False, to='plan_vuelo.flp_trafico'),
        ),
        migrations.RunSQL('ALTER TABLE plan_vuelo_flp_aprobado ALTER id_flpaprobado TYPE varchar(22);'),
    ]
