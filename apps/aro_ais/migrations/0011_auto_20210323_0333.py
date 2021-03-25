# Generated by Django 2.2.5 on 2021-03-23 03:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan_vuelo', '0010_auto_20210323_0333'),
        ('aro_ais', '0010_auto_20210317_1914'),
    ]

    operations = [
        migrations.CreateModel(
            name='Direccion_amhs',
            fields=[
                ('direccionamiento', models.CharField(max_length=8, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Prioridad',
            fields=[
                ('prioridad', models.CharField(max_length=2, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_notam',
            fields=[
                ('tipo_notam', models.CharField(max_length=6, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterModelOptions(
            name='historico_pib',
            options={'ordering': ('fecha_modificado',)},
        ),
        migrations.CreateModel(
            name='Banco_notam_charly',
            fields=[
                ('id_datanotam', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_hora_deposito', models.CharField(max_length=10)),
                ('indicador_remitente', models.CharField(max_length=8)),
                ('serie_numero_charly', models.CharField(max_length=8000)),
                ('serie_numero_alfa', models.CharField(max_length=8000)),
                ('serie_numero_charly_repla', models.CharField(max_length=8000)),
                ('serie_numero_alfa_repla', models.CharField(max_length=8000)),
                ('serie_numero_charly_cancel', models.CharField(max_length=8000)),
                ('serie_numero_alfa_cancel', models.CharField(max_length=8000)),
                ('fir', models.CharField(max_length=4)),
                ('codigo_notam_asunto', models.CharField(max_length=2)),
                ('codigo_notam_estado', models.CharField(max_length=2)),
                ('transito', models.CharField(max_length=2)),
                ('objetivo', models.CharField(max_length=3)),
                ('alcance', models.CharField(max_length=2)),
                ('limite_inferior', models.CharField(max_length=3)),
                ('limite_superior', models.CharField(max_length=3)),
                ('coordenadas', models.CharField(max_length=14)),
                ('desde', models.CharField(max_length=10)),
                ('hasta', models.CharField(max_length=10)),
                ('horario', models.CharField(max_length=35)),
                ('texto_notam', models.CharField(max_length=200)),
                ('limite_inferior_casilla', models.CharField(max_length=300)),
                ('limite_superior_casilla', models.CharField(max_length=300)),
                ('firma', models.CharField(max_length=20)),
                ('direccion', models.ManyToManyField(to='aro_ais.Direccion_amhs')),
                ('indicador_prioridad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aro_ais.Prioridad')),
                ('lugar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='plan_vuelo.Aeropuerto')),
            ],
        ),
    ]
