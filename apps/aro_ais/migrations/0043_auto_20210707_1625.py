# Generated by Django 3.1.7 on 2021-07-07 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aro_ais', '0042_notam_trafico_charly_repla_form_oaci'),
    ]

    operations = [
        migrations.AddField(
            model_name='notam_trafico_alfa_cancel',
            name='form_oaci',
            field=models.FileField(blank=True, null=True, upload_to='documents-%Y-%m-%d/'),
        ),
        migrations.AddField(
            model_name='notam_trafico_alfa_new',
            name='form_oaci',
            field=models.FileField(blank=True, null=True, upload_to='documents-%Y-%m-%d/'),
        ),
        migrations.AddField(
            model_name='notam_trafico_alfa_repla',
            name='form_oaci',
            field=models.FileField(blank=True, null=True, upload_to='documents-%Y-%m-%d/'),
        ),
        migrations.AddField(
            model_name='notam_trafico_charly_cancel',
            name='form_oaci',
            field=models.FileField(blank=True, null=True, upload_to='documents-%Y-%m-%d/'),
        ),
        migrations.AddField(
            model_name='notam_trafico_charly_new',
            name='form_oaci',
            field=models.FileField(blank=True, null=True, upload_to='documents-%Y-%m-%d/'),
        ),
    ]