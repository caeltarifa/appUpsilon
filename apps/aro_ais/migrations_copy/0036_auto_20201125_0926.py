# Generated by Django 3.1.1 on 2020-11-25 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0035_estado_asunto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asunto',
            name='id_asunto',
            field=models.CharField(max_length=3, primary_key=True, serialize=False),
        ),
    ]