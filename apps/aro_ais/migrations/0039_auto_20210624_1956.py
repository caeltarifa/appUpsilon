# Generated by Django 3.1.7 on 2021-06-24 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0038_auto_20210624_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='notam_trafico_alfa_new',
            name='est',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notam_trafico_alfa_new',
            name='perm',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notam_trafico_alfa_repla',
            name='est',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notam_trafico_alfa_repla',
            name='perm',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notam_trafico_charly_new',
            name='est',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notam_trafico_charly_new',
            name='perm',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notam_trafico_charly_repla',
            name='est',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notam_trafico_charly_repla',
            name='perm',
            field=models.BooleanField(default=False),
        ),
    ]
