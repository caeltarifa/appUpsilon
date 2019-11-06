from django.db import models

# Create your models here.

class Flp_trafico(models.Model):
    id = models.AutoField(primary_key=True)
    id_amhs = models.CharField(max_length=30)
    fecha_llegada =models.DateField()
    hora_amhs = models.CharField(max_length=10)
    prioridad = models.CharField(max_length=2)
    id_plan = models.CharField(max_length=50)
    transponder = models.CharField(max_length=60)
    origen = models.CharField(max_length=20)
    texto = models.CharField(max_length=250)
    visto = models.BooleanField(default=False) #si el modeo¿lo ha sido visto
    visto_por = models.CharField(max_length=20) #sesion que lo ha visto#

class Flp_aprobado(models.Model):
    id_plan = models.CharField(max_length=30)
    fecha_aprob = models.DateField()
    hora_aprob = models.TimeField(auto_now=True, auto_now_add=False)
    aprobado_por = models.CharField(max_length=20) # usuario que lo ha aprobado #
    #autor = models.ForeignKey(Autor)

class Flp_autor(models.Model):
    nombre = models.CharField(max_length=10)
    apellido = models.CharField(max_length=20)