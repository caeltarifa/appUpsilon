# Generated by Django 3.1.1 on 2020-09-01 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id_cargo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_cargo', models.CharField(max_length=35)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_mensaje', models.CharField(max_length=22)),
                ('aftn1', models.CharField(max_length=11)),
                ('aftn2', models.CharField(max_length=15)),
                ('id_aeronave', models.CharField(max_length=50)),
                ('reglas_vuelo', models.CharField(max_length=50)),
                ('aeropuerto_salida', models.CharField(max_length=9)),
                ('ruta', models.CharField(max_length=100)),
                ('aeropuerto_destino', models.CharField(max_length=30)),
                ('otros', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Ruta_flp',
            fields=[
                ('id_ruta', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_ruta', models.CharField(max_length=25)),
                ('ruta', models.CharField(max_length=900)),
            ],
        ),
        migrations.CreateModel(
            name='Ruta_guardada',
            fields=[
                ('id_ruta', models.AutoField(primary_key=True, serialize=False)),
                ('rutas', models.CharField(max_length=30)),
                ('puntos_limite', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('ci', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=35)),
                ('apellido', models.CharField(max_length=35)),
                ('activo', models.BooleanField(default=True)),
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
                ('puntoInicial', models.CharField(max_length=35)),
                ('puntoFinal', models.CharField(max_length=35)),
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
                ('id_flp_aprobado', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='plan_vuelo.flp_trafico')),
                ('fecha_aprobacion', models.DateField()),
                ('hora_aprobacion', models.TimeField(auto_now=True)),
                ('transponder', models.IntegerField()),
                ('ruta_usada', models.CharField(max_length=250)),
                ('puntos_de_ficha', models.CharField(max_length=200)),
                ('matricula', models.CharField(max_length=10)),
                ('controlador', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='plan_vuelo.trabajador')),
            ],
        ),
    ]
