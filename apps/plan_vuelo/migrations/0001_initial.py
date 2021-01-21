# Generated by Django 3.1.5 on 2021-01-13 14:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aeropuerto',
            fields=[
                ('aeropuerto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('iata', models.CharField(max_length=5)),
                ('icao', models.CharField(max_length=4)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
            ],
            options={
                'ordering': ['aeropuerto'],
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id_cargo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_cargo', models.CharField(max_length=35)),
                ('cuenta_usuario', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa_institucion',
            fields=[
                ('id_emp_inst', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_emp_inst', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Flp_trafico',
            fields=[
                ('id_mensaje', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('aftn1', models.CharField(max_length=11)),
                ('aftn2', models.CharField(max_length=15)),
                ('id_aeronave', models.CharField(max_length=50)),
                ('reglas_vuelo', models.CharField(max_length=50)),
                ('aeropuerto_salida', models.CharField(max_length=9)),
                ('ruta', models.CharField(max_length=100)),
                ('aeropuerto_destino', models.CharField(max_length=30)),
                ('otros', models.CharField(max_length=500)),
                ('aprobado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Notam_trafico',
            fields=[
                ('id_mensaje', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('aftn1', models.CharField(max_length=11)),
                ('aftn2', models.CharField(max_length=15)),
                ('idnotam', models.CharField(max_length=85)),
                ('resumen', models.CharField(max_length=65)),
                ('aplica_a', models.CharField(max_length=15)),
                ('valido_desde', models.CharField(max_length=20)),
                ('valido_hasta', models.CharField(max_length=20)),
                ('mensaje', models.CharField(max_length=450)),
                ('nuevo', models.BooleanField(default=True)),
                ('ingresado', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
            ],
            options={
                'ordering': ['idnotam'],
            },
        ),
        migrations.CreateModel(
            name='Punto_satelital',
            fields=[
                ('nombrepunto', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
                'ordering': ['nombrepunto'],
            },
        ),
        migrations.CreateModel(
            name='Ruta_flp',
            fields=[
                ('id_ruta', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_ruta', models.CharField(max_length=25)),
                ('ruta', models.CharField(max_length=900)),
            ],
            options={
                'ordering': ['nombre_ruta'],
            },
        ),
        migrations.CreateModel(
            name='Ruta_guardada',
            fields=[
                ('id_ruta', models.AutoField(primary_key=True, serialize=False)),
                ('origen', models.CharField(max_length=4)),
                ('destino', models.CharField(max_length=4)),
                ('rutas', models.CharField(max_length=30)),
                ('puntos_limite', models.CharField(max_length=60)),
                ('archivada', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('ci', models.IntegerField(primary_key=True, serialize=False)),
                ('coordinador', models.BooleanField(default=False)),
                ('nombre', models.CharField(max_length=35)),
                ('apellido', models.CharField(max_length=35)),
                ('activo', models.BooleanField(default=False)),
                ('correo', models.EmailField(blank=True, max_length=30)),
                ('codigo', models.CharField(blank=True, max_length=4)),
                ('cargo', models.ManyToManyField(to='plan_vuelo.Cargo')),
                ('empresa_institucion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='plan_vuelo.empresa_institucion')),
            ],
        ),
        migrations.CreateModel(
            name='EntrePuntos_flp',
            fields=[
                ('id_segmento', models.AutoField(primary_key=True, serialize=False)),
                ('puntoinicial', models.CharField(max_length=35)),
                ('puntofinal', models.CharField(max_length=35)),
                ('distancia', models.IntegerField()),
                ('nivelCrucero', models.CharField(max_length=6)),
                ('ruta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan_vuelo.ruta_flp')),
            ],
            options={
                'ordering': ['id_segmento', 'ruta'],
            },
        ),
        migrations.AddField(
            model_name='cargo',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='plan_vuelo.empresa_institucion'),
        ),
        migrations.CreateModel(
            name='Flp_aprobado',
            fields=[
                ('id_flpaprobado', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='xxxx', serialize=False, to='plan_vuelo.flp_trafico')),
                ('fecha_aprobacion', models.DateField(auto_now=True)),
                ('hora_aprobacion', models.TimeField(auto_now=True)),
                ('transponder', models.IntegerField()),
                ('ruta_usada', models.CharField(max_length=250)),
                ('puntos_de_ficha', models.CharField(max_length=200)),
                ('matricula', models.CharField(max_length=10)),
                ('tiempos', models.CharField(max_length=100)),
                ('frecuencias', models.CharField(max_length=10)),
                ('nivel', models.CharField(max_length=6)),
                ('por_trabajar', models.BooleanField(default=True)),
                ('en_curso', models.BooleanField(default=False)),
                ('finalizado', models.BooleanField(default=False)),
                ('controlador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='plan_vuelo.trabajador')),
            ],
        ),
    ]
