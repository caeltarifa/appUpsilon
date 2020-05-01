from django.db import models

# Create your models here.
from apps.plan_vuelo.models import Trabajador

class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True,blank=False)
    nombre_estado = models.CharField(max_length=20,blank=False)
    descripcion =models.CharField(max_length=60,blank=False)
    def __str__(self):
        return '{}/{}'.format(
            self.id_estado,
            self.nombre_estado,
            self.descripcion
            )
#solicitado, cancelado, aprobado_ais, aprobado_policia, rechazado_ais, rechazado_policia

class Comunicacional(models.Model):
    id_comunicacion = models.AutoField(primary_key=True)
    direcciones_amhs = models.CharField(max_length=100,blank=False)
    originador_amhs = models.CharField(max_length=8,blank=False)
    fecha_hora_deposito = models.CharField(max_length=6,blank=False) #23 14:40:23;; 23 14:45:23
    tiempo_utc_modific = models.CharField(max_length=19,blank=False) #23/03/2020 14:40:23
    def __str__(self):
        return '{}/{}'.format(self.id_comunicacion, self.direcciones_amhs, self.originador_amhs, self.fecha_hora_deposito)

class Operacional(models.Model):
    id_operacional=models.AutoField(primary_key=True)
    id_aeronave=models.CharField(max_length=7,blank=False) #identificacion aeronave
    regla_vuelo=models.CharField(max_length=1,blank=False)
    tipo_vuelo=models.CharField(max_length=1,blank=False)
    numero=models.CharField(max_length=2,blank=False)
    tipo_aeronave=models.CharField(max_length=4,blank=False)
    estela_turbulenta=models.CharField(max_length=1,blank=False)
    equipoA=models.CharField(max_length=100,blank=False)
    equipoB=models.CharField(max_length=100,blank=False)
    aerodromo_salida=models.CharField(max_length=4,blank=False)
    hora_salida=models.CharField(max_length=4,blank=False)
    velocidad_crucero_cat=models.CharField(max_length=1,blank=False)
    velocidad_crucero=models.CharField(max_length=5,blank=False)
    nivel_cat=models.CharField(max_length=1,blank=False)
    nivel=models.CharField(max_length=4,blank=False)
    ruta=models.CharField(max_length=100,blank=False)
    aerodromo_destino=models.CharField(max_length=4,blank=False)
    total_eet=models.CharField(max_length=4,blank=False)
    aerodromo_alterno=models.CharField(max_length=4,blank=True)
    aerodromo_alterno2=models.CharField(max_length=4,blank=True)
    otros_datos=models.CharField(max_length=250,blank=True)
    def __str__(self):
        return '{}/{}'.format(
                self.id_operacional,
                self.id_aeronave,
                self.regla_vuelo,
                self.tipo_vuelo,
                self.numero,
                self.tipo_aeronave,
                self.estela_turbulenta,
                self.equipoA,
                self.equipoB,
                self.aerodromo_salida,
                self.hora_salida,
                self.velocidad_crucero_cat,
                self.velocidad_crucero,
                self.nivel_cat,
                self.nivel,
                self.ruta,
                self.aerodromo_destino,
                self.total_eet,
                self.aerodromo_alterno,
                self.aerodromo_alterno2,
                self.otros_datos
                )

class Suplementaria(models.Model):
    id_suplementaria=models.AutoField(primary_key=True)
    
    autonomia_hr_min=models.CharField(max_length=4)
    personas_bordo=models.CharField(max_length=3)
    equipo_radio_uhf=models.BooleanField(default=False) #uhf vhf elt
    equipo_radio_vhf=models.BooleanField(default=False)
    equipo_radio_elt=models.BooleanField(default=False)
    
    equipo_superv=models.BooleanField(default=False) 
    equipo_superv_polar=models.BooleanField(default=False) 
    equipo_superv_deser=models.BooleanField(default=False) 
    equipo_superv_mar=models.BooleanField(default=False) 
    equipo_superv_jung=models.BooleanField(default=False) 

    chaleco=models.BooleanField(default=False) 
    chaleco_luz=models.BooleanField(default=False) 
    chaleco_fluor=models.BooleanField(default=False) 
    chaleco_uhf=models.BooleanField(default=False) 
    chaleco_vhf=models.BooleanField(default=False) 

    nro_botes=models.IntegerField(blank=True)
    capacidad_botes=models.CharField(max_length=3,blank=True)
    color_bote=models.CharField(max_length=30,blank=True)
    color_marca_avion=models.CharField(max_length=70)
    obs=models.CharField(max_length=100,blank=True)
    piloto=models.CharField(max_length=60)
    requisitos_adic=models.CharField(max_length=200,blank=True)
    def __str__(self):
        return '{}/{}'.format(
            self.autonomia_hr_min,
            self.personas_bordo,
            self.equipo_radio_uhf,
            self.equipo_radio_vhf,
            self.equipo_radio_elt,
            self.equipo_superv,
            self.equipo_superv_polar,
            self.equipo_superv_deser,
            self.equipo_superv_mar,
            self.equipo_superv_jung,
            self.chaleco,
            self.chaleco_luz,
            self.chaleco_fluor,
            self.chaleco_uhf,
            self.chaleco_vhf,
            self.nro_botes,
            self.capacidad_botes,
            self.color_bote,
            self.color_marca_avion,
            self.obs,
            self.piloto,
            self.requisitos_adic
                )

class Plan_vuelo_presentado(models.Model):
    id_fpl_presentado=models.AutoField(primary_key=True)
    nro_formulario=models.IntegerField()#EL SISTEMA ASIGNA AUTOMATICAMENTE
    fecha_presentacion = models.DateField()#EL SISTEMA ASIGNA AUTOMATICAMENTE
    hora_presentacion = models.CharField(max_length=10,blank=False)
    
    arg_rechazo_policia = models.CharField(max_length=50,blank=True)
    arg_rechazo_ais = models.CharField(max_length=50,blank=True)
    
    date_estado_ais = models.CharField(max_length=200,blank=True) #REGISTRO DE TIEMPO DE MODIFICACIONES 23-02-2020 16:45:12;;23-02-2020 16:45:12;;
    date_estado_policia = models.CharField(max_length=200,blank=True) ##REGISTRO DE TIEMPO DE MODIFICACIONES 23-02-2020 16:45:12;;23-02-2020 16:45:12;;
    
    parte_comunicacional = models.OneToOneField(
        Comunicacional,
        on_delete=models.PROTECT,
        primary_key=False,
        null=True,
        blank=True,
        related_name='pcomunic+',
        db_column="parte_comunicacional_id"
    )
    parte_operacional = models.OneToOneField(
        Operacional,
        on_delete=models.PROTECT,
        primary_key=False,
        null=True,
        blank=True,
        related_name='poperac+',
        db_column="parte_operacional_id"
    )
    parte_suplementaria = models.OneToOneField(
        Suplementaria,
        on_delete=models.PROTECT,
        primary_key=False,
        null=True,
        blank=True,
        related_name='psuple+',
        db_column="parte_suplementaria_id"
    )
    #DESPACHADOR, POLICIA, AIS, COMUNICADOR
    fk_despachador = models.ForeignKey(
        Trabajador,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='despa+', #para no tener relaciones al reves
        db_column="fk_despachador_id"
    )
    fk_policia = models.ForeignKey(
        Trabajador,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='poli+',
        db_column="fk_policia_id"
    )
    fk_ais = models.ForeignKey(
        Trabajador,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='ais+',
        db_column="fk_ais_id"
    )
    fk_comunicador = models.ForeignKey(
        Trabajador,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='com+',
        db_column="fk_comunicador_id"
    )
    fk_estado = models.ForeignKey(
        Estado,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='estado+',
        db_column="fk_estado_id"
    )
    hora_cancel_expir = models.CharField(max_length=10,blank=True)#registra la hora cancelada o expirada


    def __str__(self):
        return '{}/{}'.format(
            self.id_fpl_presentado,
            self.nro_formulario,
            self.fecha_presentacion,
            self.arg_rechazo_policia,
            self.arg_rechazo_ais,
            self.date_estado_ais,
            self.date_estado_policia,
            self.parte_comunicacional,
            self.parte_operacional,
            self.parte_suplementaria,
            self.fk_despachador,
            self.fk_policia,
            self.fk_ais,
            self.fk_comunicador,
            self.fk_estado,
            self.hora_cancel_expir,
                )