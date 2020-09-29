# Generated by Django 3.1.1 on 2020-09-28 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0018_auto_20200928_0505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pib_extenso',
            name='agendado',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='alcance',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='area',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='cuerpo',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='fir',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='fl_inferior',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='fl_superior',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='indices_item_a',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='indices_item_b',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='indices_item_c',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='indices_item_d',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='indices_item_e',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='indices_item_f',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='indices_item_g',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='limit_inferior',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='limit_superior',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='lugar',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='notam_codigo',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='notam_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='notam_tipo',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='proposito',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='ref_notam_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pib_extenso',
            name='tipo_trafico',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
