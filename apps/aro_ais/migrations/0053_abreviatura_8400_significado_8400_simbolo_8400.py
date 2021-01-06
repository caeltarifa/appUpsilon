# Generated by Django 3.1.1 on 2020-12-03 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0052_auto_20201203_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Significado_8400',
            fields=[
                ('id_significado', models.AutoField(primary_key=True, serialize=False)),
                ('significado_completo', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Simbolo_8400',
            fields=[
                ('id_simbolo', models.AutoField(primary_key=True, serialize=False)),
                ('simbolo', models.CharField(max_length=2)),
                ('descripcion', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Abreviatura_8400',
            fields=[
                ('abreviatura', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('significado_pib', models.CharField(max_length=400)),
                ('significado_completo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aro_ais.significado_8400')),
                ('simbolo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aro_ais.simbolo_8400')),
            ],
        ),
    ]
