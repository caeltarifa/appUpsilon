# Generated by Django 2.2.5 on 2019-11-09 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flp_aprobado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_plan', models.CharField(max_length=30)),
                ('fecha_aprob', models.DateField()),
                ('hora_aprob', models.TimeField(auto_now=True)),
                ('aprobado_por', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Flp_autor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=10)),
                ('apellido', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Flp_trafico',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_amhs', models.CharField(max_length=30)),
                ('fecha_llegada', models.DateField()),
                ('hora_amhs', models.CharField(max_length=10)),
                ('prioridad', models.CharField(max_length=2)),
                ('id_plan', models.CharField(max_length=50)),
                ('transponder', models.CharField(max_length=60)),
                ('origen', models.CharField(max_length=20)),
                ('texto', models.CharField(max_length=250)),
                ('visto', models.BooleanField(default=False)),
                ('visto_por', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Metar_trafico',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_amhs', models.CharField(max_length=30)),
                ('fecha_llegada', models.DateField()),
                ('hora_amhs', models.CharField(max_length=10)),
                ('prioridad', models.CharField(max_length=2)),
                ('estacion', models.CharField(max_length=50)),
                ('hora_clima', models.CharField(max_length=60)),
                ('texto', models.CharField(max_length=1000)),
                ('visto', models.BooleanField(default=False)),
                ('visto_por', models.CharField(max_length=20)),
            ],
        ),
    ]
