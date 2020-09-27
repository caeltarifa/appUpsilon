
from django.db import models
from datetime import datetime

from apps.plan_vuelo.models import  Notam_trafico, Trabajador

# Create your models here.


class Pib_trafico(models.Model):
    pib_notam = models.OneToOneField(
        Notam_trafico,
        #related_name='xxxx',
        on_delete=models.PROTECT,
        primary_key=True,
    )

    fir = models.CharField(max_length=20, blank=False, null=False)
    instalacion = models.CharField(max_length=30, blank=False, null=False)
    informacion = models.CharField(max_length=900, blank=False, null=False)
    publicado = models.BooleanField(default=False)
    vigente = models.BooleanField(default=False)
    archivado = models.BooleanField(default=False)

    inicio_publi = models.DateField(blank=True, null=True)
    fin_publi = models.DateField(blank=True, null=True)
    
    oficialaro = models.ForeignKey(Trabajador,on_delete=models.PROTECT, blank=False, null=False) 
    
    def __unicode__(self):
        return self.pib_notam
    class Meta:
        ordering = ['fir']

