# Generated by Django 3.1.1 on 2020-11-25 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0029_auto_20201011_2356'),
    ]

    operations = [
        migrations.CreateModel(
            name='Letra_asunto',
            fields=[
                ('id_letra', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('descripcion_letra', models.CharField(max_length=350)),
                ('acronimo', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Estado_asunto',
            fields=[
                ('id_estado_asunto', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('descripcion_estado', models.CharField(max_length=350)),
                ('fasiologia_estado', models.CharField(max_length=20)),
                ('letra_asunto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aro_ais.letra_asunto')),
            ],
        ),
        migrations.CreateModel(
            name='Asunto',
            fields=[
                ('id_asunto', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('descripcion_asunto', models.CharField(max_length=350)),
                ('fasiologia_asunto', models.CharField(max_length=20)),
                ('letra_asunto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aro_ais.letra_asunto')),
            ],
        ),
    ]
