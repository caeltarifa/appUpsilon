from django.db import models

# Create your models here.
#from apps.generacion_fpl.models import Empresa_institucion


#class Metar_trafico(models.Model):
#    id = models.AutoField(primary_key=True)
#    id_amhs = models.CharField(max_length=30)
#    fecha_llegada =models.DateField()
#    hora_amhs = models.CharField(max_length=10)
#    prioridad = models.CharField(max_length=2)
#    estacion = models.CharField(max_length=50)
#    hora_clima = models.CharField(max_length=60)
#    texto = models.CharField(max_length=1000)
#    visto = models.BooleanField(default=False) #si el modeo¿lo ha sido visto
#    visto_por = models.CharField(max_length=20) #sesion que lo ha visto#

class Empresa_institucion(models.Model):
    id_emp_inst=models.AutoField(primary_key=True)
    nombre_emp_inst=models.CharField(max_length=50)
    def __str__(self):
        return self.nombre_emp_inst

class Cargo(models.Model):
    id_cargo=models.AutoField(primary_key=True)
    nombre_cargo=models.CharField(max_length=35)
    empresa = models.ForeignKey(Empresa_institucion, on_delete=models.PROTECT)
    def __str__(self):
        return self.nombre_cargo

class Flp_trafico(models.Model):
    id_mensaje = models.CharField(max_length=22,primary_key=True)
    aftn1 = models.CharField(max_length=11)
    aftn2 = models.CharField(max_length=15)
    id_aeronave = models.CharField(max_length=50)
    reglas_vuelo = models.CharField(max_length=50)
    aeropuerto_salida = models.CharField(max_length=9)
    ruta = models.CharField(max_length=100)
    aeropuerto_destino = models.CharField(max_length=30)
    otros = models.CharField(max_length=500) #si el modeo¿lo ha sido visto
    aprobado = models.BooleanField(default=False)

class Trabajador(models.Model):
    ci=models.IntegerField(primary_key=True)
    nombre=models.CharField(max_length=35)
    apellido = models.CharField(max_length=35)
    activo=models.BooleanField(default=True)
    empresa_institucion = models.ForeignKey(Empresa_institucion, on_delete=models.PROTECT)
    cargo=models.ManyToManyField(Cargo)
    correo=models.EmailField(max_length=30,blank=True)
    codigo=models.CharField(max_length=4,blank=True)
    def __str__(self):
        return '{}/{}'.format(self.nombre, self.apellido, self.empresa_institucion.nombre_emp_inst)

class Flp_aprobado(models.Model):
    #id_aprobado = models.AutoField(primary_key=True)
    id_flpaprobado = models.OneToOneField(
        Flp_trafico,
        related_name='xxxx',
        on_delete=models.PROTECT,
        primary_key=True,
    )
    controlador = models.ForeignKey(Trabajador,on_delete=models.PROTECT,)
    fecha_aprobacion = models.DateField(auto_now=True, auto_now_add=False)
    hora_aprobacion = models.TimeField(auto_now=True, auto_now_add=False)
    transponder = models.IntegerField()
    ruta_usada = models.CharField(max_length=250) #almacena punto1-ruta-punto2, punto3-ruta-punto4, 
    puntos_de_ficha = models.CharField(max_length=200) #almacena los puntos usados en los unicodeips y longitude: 'punto1 23 punto2 34 punto3 56 punto4'
    matricula = models.CharField(max_length=10) #almacena matricula de avion
    tiempos = models.CharField(max_length=100)
    frecuencias = models.CharField(max_length=10)
    nivel = models.CharField(max_length=6)
    def __unicode__(self):
        return '%s %s' % (self.id_flp_aprobado, self.metar_trafico, self.controlador)

class Ruta_guardada(models.Model):
    id_ruta = models.AutoField(primary_key=True)
    origen = models.CharField(max_length=4)
    destino = models.CharField(max_length=4)
    rutas = models.CharField(max_length=30)
    puntos_limite = models.CharField(max_length=60)
    archivada = models.BooleanField(default=False)
    def __unicode__(self):
        return self.id_ruta, self.rutas
    
        #{
        #    'id_ruta': self.id_ruta,
        #    'rutas': self.rutas,
        #}

##RUTA , SEGMENTO DE LA RUTA Y DISTANCIAS ENTRE PUNTOS DE LA RUTA
class Ruta_flp(models.Model):
    id_ruta=models.AutoField(primary_key=True)
    nombre_ruta=models.CharField(max_length=25)
    ruta=models.CharField(max_length=900)
    
    def detectar_numeros(self, lista):
        listares=[]
        for x in lista:
            if x.isdigit():
                listares.append(int(x))
            else:
                listares.append(x)
        return listares

    def subruta_puntos(self, anterior, lista_puntos, siguiente):
        if (anterior in lista_puntos) and (siguiente in lista_puntos):
            if lista_puntos.index(anterior) > lista_puntos.index(siguiente):
                lista_puntos.reverse()
            lista_puntos = self.detectar_numeros(lista_puntos[lista_puntos.index(anterior): lista_puntos.index(siguiente)+1] )
            return lista_puntos
        else:
            if anterior in lista_puntos:
                return [anterior]
            if siguiente in lista_puntos:
                return [siguiente]
            return []
    
    def detectarRutas(self, listax):
        lista_rutas=[]
        lista_ruta_puntos=[]

        if len(listax) > 0:
            contador=0
            for punto in listax:
                if Ruta_flp.objects.filter(nombre_ruta=punto).exists():
                    lista_rutas.append(Ruta_flp.objects.filter(nombre_ruta=punto)[0])
                    puntos_ruta = Ruta_flp.objects.filter(nombre_ruta=punto)[0].ruta.split(";;")
                    if contador==0:
                        siguiente=listax[contador+1]
                        lista_ruta_puntos.append([siguiente])
                    else:
                        if contador==(len(listax)-1):
                            anterior=listax[contador-1]
                            lista_ruta_puntos.append([anterior])
                        else:
                            anterior=listax[contador-1]
                            siguiente=listax[contador+1]
                            lista_ruta_puntos.append(self.subruta_puntos(anterior, puntos_ruta, siguiente))
                contador=contador+1
        return lista_rutas,lista_ruta_puntos
    
    def getMatricula(self, cadena):
        matricula=''
        try:
            indice=cadena.index('REG/')+4
            for x in range(indice, len(cadena)):
                if cadena[x]!=' ':
                    matricula+=cadena[x]
                else:
                    break
        except ValueError:
            matricula='NFound'
        
        return matricula
        

    def getTransmision(self, cadena):
        transmision=''
        try:
            indice=cadena.index('SEL/')+4
            for x in range(indice, len(cadena)):
                if cadena[x]!=' ':
                    transmision+=cadena[x]
                else:
                    break
        except ValueError:
            transmision='NFound'

        return transmision

    def __unicode__(self):
        return '%s %s' % (self.id_ruta, self.nombre_ruta, self.ruta)

class EntrePuntos_flp(models.Model):
    id_segmento=models.AutoField(primary_key=True)
    ruta=models.ForeignKey(Ruta_flp, on_delete=models.CASCADE)
    puntoinicial=models.CharField(max_length=35)
    puntofinal=models.CharField(max_length=35)
    distancia=models.IntegerField()
    nivelCrucero=models.CharField(max_length=6)
    
    def __unicode__(self):
        return self.id_segmento, self.ruta

    class Meta:
        ordering = ['id_segmento','ruta']

class Punto_satelital(models.Model):
    nombrepunto = models.CharField(max_length=10,primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __unicode__(self):
        return self.nombrepunto

    class Meta:
        ordering = ['nombrepunto']