# Generated by Django 3.1.5 on 2021-03-17 18:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0007_delete_historico_pib'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historico_pib',
            fields=[
                ('id_pib_historico', models.AutoField(primary_key=True, serialize=False)),
                ('lista_notam', models.CharField(max_length=35)),
                ('fecha_modificado', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'ordering': ('id_pib_historico',),
            },
        ),
    ]
