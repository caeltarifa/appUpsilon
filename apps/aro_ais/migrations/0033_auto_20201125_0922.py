# Generated by Django 3.1.1 on 2020-11-25 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0032_auto_20201125_0912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estado_asunto',
            name='letra_asunto',
        ),
        migrations.AddField(
            model_name='estado_asunto',
            name='asunto',
            field=models.ForeignKey(default='dsa', on_delete=django.db.models.deletion.PROTECT, to='aro_ais.asunto'),
            preserve_default=False,
        ),
    ]
