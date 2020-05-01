from django.db import models

# Create your models here.
#from apps.generacion_fpl.models import Empresa_institucion

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

class Metar_trafico(models.Model):
    id = models.AutoField(primary_key=True)
    id_amhs = models.CharField(max_length=30)
    fecha_llegada =models.DateField()
    hora_amhs = models.CharField(max_length=10)
    prioridad = models.CharField(max_length=2)
    estacion = models.CharField(max_length=50)
    hora_clima = models.CharField(max_length=60)
    texto = models.CharField(max_length=1000)
    visto = models.BooleanField(default=False) #si el modeo¿lo ha sido visto
    visto_por = models.CharField(max_length=20) #sesion que lo ha visto#

class Empresa_institucion(models.Model):
    id_emp_inst=models.AutoField(primary_key=True)
    nombre_emp_inst=models.CharField(max_length=50)
    def __str__(self):
        return self.nombre_emp_inst

class Cargo(models.Model):
    id_cargo=models.AutoField(primary_key=True)
    nombre_cargo=models.CharField(max_length=35)
    def __str__(self):
        return self.nombre_cargo

class Trabajador(models.Model):
    ci=models.IntegerField(primary_key=True)
    nombre=models.CharField(max_length=35)
    apellido = models.CharField(max_length=35)
    activo=models.BooleanField(default=True)
    empresa_institucion = models.ForeignKey(Empresa_institucion, on_delete=models.PROTECT)
    cargo=models.ManyToManyField(Cargo)
    correo=models.EmailField(max_length=30)
    codigo=models.CharField(max_length=4)
    def __str__(self):
        return '{}/{}'.format(self.nombre, self.apellido, self.empresa_institucion.nombre_emp_inst)

class Flp_aprobado(models.Model):
    #id_aprobado = models.AutoField(primary_key=True)
    id_flp_aprobado = models.OneToOneField(
        Flp_trafico,
        on_delete=models.PROTECT,
        primary_key=True,
    )
    metar_trafico = models.OneToOneField(
        Metar_trafico,
        on_delete=models.PROTECT,
        primary_key=False,
    )
    controlador = models.OneToOneField(
        Trabajador,
        on_delete=models.PROTECT,
        primary_key=False,
    )
    fecha_aprob = models.DateField()
    hora_aprob = models.TimeField(auto_now=True, auto_now_add=False)
    transponder = models.IntegerField()
    ruta_usada = models.CharField(max_length=250) #almacena punto1-ruta-punto2, punto3-ruta-punto4, 
    puntos_de_ficha = models.CharField(max_length=400) #almacena los puntos usados en los unicodeips y longitude: 'punto1 23 punto2 34 punto3 56 punto4'
    matricula = models.CharField(max_length=400) #almacena matricula de avion
    def __unicode__(self):
        return '%s %s' % (self.id_flp_aprobado, self.metar_trafico, self.controlador)


##RUTA , SEGMENTO DE LA RUTA Y DISTANCIAS ENTRE PUNTOS DE LA RUTA
class Ruta_flp(models.Model):
    id_ruta=models.AutoField(primary_key=True)
    nombre_ruta=models.CharField(max_length=25)
    ruta=models.CharField(max_length=900)
    
    def __unicode__(self):
        return '%s %s' % (self.id_ruta, self.nombre_ruta, self.ruta)

class EntrePuntos_flp(models.Model):
    id_segmento=models.AutoField(primary_key=True)
    ruta=models.ForeignKey(Ruta_flp, on_delete=models.CASCADE)
    puntoInicial=models.CharField(max_length=35)
    puntoFinal=models.CharField(max_length=35)
    distancia=models.IntegerField()
    nivelCrucero=models.CharField(max_length=6)
    
    def __unicode__(self):
        return self.id_segmento, self.ruta

    class Meta:
        ordering = ['id_segmento','ruta']