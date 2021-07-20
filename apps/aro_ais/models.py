
from django.db import models
from datetime import datetime

from apps.plan_vuelo.models import Notam_trafico
from apps.plan_vuelo.models import Trabajador
from apps.plan_vuelo.models import Aeropuerto

# Create your models here.


class Pib_trafico(models.Model):
    ref_notam_amhs = models.OneToOneField(
        Notam_trafico,
        # related_name='xxxx',
        on_delete=models.PROTECT,
        primary_key=True,
    )

    oficialaro = models.ForeignKey(
        Trabajador, on_delete=models.PROTECT, blank=True, null=True)

    decodificado = models.CharField(max_length=600)

    publicado = models.DateTimeField(blank=True, null=True)
    vigente = models.BooleanField(default=False)
    archivado = models.BooleanField(default=False)
    pendiente = models.BooleanField(default=True)

    msj_publicado = models.CharField(max_length=600, blank=True, null=True)
    instalacion = models.CharField(max_length=60, blank=True, null=True)

    def __unicode__(self):
        return self.ref_notam_amhs

    class Meta:
        ordering = ['ref_notam_amhs']


class Pib_extenso(models.Model):
    notam_extenso = models.OneToOneField(
        Pib_trafico,
        # related_name='xxxx',
        on_delete=models.PROTECT,
        primary_key=True,
    )

    # notam_id   A3465/19              <class 'str'>
    notam_id = models.CharField(max_length=70, blank=True, null=True)
    # notam_type   NEW              <class 'str'>
    notam_tipo = models.CharField(max_length=10, blank=True, null=True)
    # ref_notam_id   None              <class 'NoneType'>
    ref_notam_id = models.CharField(max_length=10, blank=True, null=True)
    # fir   SPIM              <class 'str'>
    fir = models.CharField(max_length=10, blank=True, null=True)
    # notam_code   QRALW              <class 'str'>
    notam_codigo = models.CharField(max_length=10, blank=True, null=True)
    # traffic_type   {'IFR', 'VFR'}              <class 'set'>
    tipo_trafico = models.CharField(max_length=50, blank=True, null=True)

    # purpose   {'OPERATIONAL SIGNIFICANCE', 'FLIGHT OPERATIONS', 'IMMEDIATE ATTENTION'}              <class 'set'>
    proposito = models.CharField(max_length=200, blank=True, null=True)
    # scope   {'NAV WARNING'}              <class 'set'>
    alcance = models.CharField(max_length=100, blank=True, null=True)

    # fl_lower   0              <class 'int'>
    fl_inferior = models.IntegerField(blank=True, null=True)
    # fl_upper   30              <class 'int'>
    fl_superior = models.IntegerField(blank=True, null=True)

    # area   {'lat': '1218S', 'long': '07654W', 'radius': 0}              <class 'dict'>
    area = models.CharField(max_length=100, blank=True, null=True)

    # location   ['SPJC']              <class 'list'>
    lugar = models.CharField(max_length=50, blank=True, null=True)
    # valid_from   2019-07-25 13:30:00+00:00      <class 'datetime.datetime'>
    valid_desde = models.DateTimeField(blank=True, null=True)
    # valid_till   2019-07-29 20:00:00+00:00      <class 'datetime.datetime'>
    valid_hasta = models.DateTimeField(blank=True, null=True)
    # schedule   DAYS 25,26,27 AND 29 BTN 1330-2000              <class 'str'>
    agendado = models.CharField(max_length=150, blank=True, null=True)

    # body   AIR PARADE DUE TO PERUVIAN INDEPENDENCE DAY. RPAS/DRONES/PARAGLIDERS AND SPORTS ACTIVITIES ARE PROHIBITED. ALL FLT HAVE TO AVOID OVERFLY. PREVIOUS COOR BTN LAS PALMAS TWR AND ACC LIMA IS REQUIRED. COORD: 121806S0765410W 121230S0770340W 120605S077044W 120332S0770238W 120457S0765829W              <class 'str'>
    cuerpo = models.CharField(max_length=400, blank=True, null=True)

    # limit_lower   GND              <class 'str'>
    limit_superior = models.CharField(max_length=10, blank=True, null=True)
    # limit_upper   3000FT              <class 'str'>
    limit_inferior = models.CharField(max_length=10, blank=True, null=True)
    # indices_item_a   (66, 70)              <class 'tuple'>
    indices_item_a = models.CharField(max_length=15, blank=True, null=True)
    # indices_item_b   (75, 85)              <class 'tuple'>
    indices_item_b = models.CharField(max_length=15, blank=True, null=True)
    # indices_item_c   (89, 99)              <class 'tuple'>
    indices_item_c = models.CharField(max_length=15, blank=True, null=True)
    # indices_item_d   (103, 137)              <class 'tuple'>
    indices_item_d = models.CharField(max_length=15, blank=True, null=True)
    # indices_item_e   (141, 423)              <class 'tuple'>
    indices_item_e = models.CharField(max_length=15, blank=True, null=True)
    # indices_item_f   (427, 430)              <class 'tuple'>
    indices_item_f = models.CharField(max_length=15, blank=True, null=True)
    # indices_item_g   (434, 440)              <class 'tuple'>
    indices_item_g = models.CharField(max_length=15, blank=True, null=True)

    def __unicode__(self):
        return self.notam_id

    class Meta:
        ordering = ['notam_id']


class Pib_registro_documento(models.Model):
    id_registropib = models.AutoField(primary_key=True)
    fecha_generado = models.DateTimeField(
        default=datetime.now, blank=True, null=True)
    registro = models.ManyToManyField(Pib_trafico)

    oficialaro = models.ForeignKey(
        Trabajador, on_delete=models.PROTECT, blank=False, null=False)

    def __unicode__(self):
        return self.fecha_generado

    class Meta:
        ordering = ['fecha_generado']


class Letra_asunto(models.Model):
    id_letra = models.CharField(max_length=1, primary_key=True)
    titulo_letra = models.CharField(max_length=350, blank=False, null=False)
    acronimo = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return '{}/{}'.format(self.id_letra, self.acronimo)

    class Meta:
        ordering = ('id_letra',)


class Asunto(models.Model):
    id_asunto = models.CharField(max_length=2, primary_key=True)
    descripcion_asunto = models.CharField(
        max_length=350, blank=False, null=False)
    fraseologia_asunto = models.CharField(
        max_length=150, blank=False, null=False)
    letra_asunto = models.ForeignKey(
        Letra_asunto, on_delete=models.PROTECT, blank=False, null=False)

    def __str__(self):
        return '{}/{}'.format(self.id_asunto, self.fraseologia_asunto)

    class Meta:
        ordering = ('id_asunto',)


class Estado_asunto(models.Model):
    id_estado_asunto = models.CharField(max_length=3, primary_key=True)
    descripcion_estado = models.CharField(
        max_length=350, blank=False, null=False)
    fraseologia_estado = models.CharField(
        max_length=150, blank=True, null=True)
    id_asunto = models.ManyToManyField(Asunto)

    def __str__(self):
        return '{}/{}'.format(self.id_estado_asunto, self.descripcion_estado)

    class Meta:
        ordering = ('id_estado_asunto',)


class Simbolo_8400(models.Model):
    id_simbolo = models.AutoField(primary_key=True)
    simbolo = models.CharField(max_length=2, blank=False, null=False)
    descripcion = models.CharField(max_length=150, blank=False, null=False)

    def __str__(self):
        return '{}__{}'.format(self.id_simbolo, self.simbolo)

    class Meta:
        ordering = ('id_simbolo',)


class Abreviatura_8400(models.Model):
    abreviatura = models.CharField(primary_key=True, max_length=15)
    simbolo = models.ManyToManyField(Simbolo_8400, blank=False)
    #simbolo = models.ForeignKey(Simbolo_8400,on_delete=models.PROTECT, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.abreviatura)

    class Meta:
        ordering = ('abreviatura',)


class Significado_8400(models.Model):
    id_significado = models.AutoField(primary_key=True)
    abreviatura = models.ForeignKey(
        Abreviatura_8400, on_delete=models.PROTECT, blank=False, null=False)
    significado_completo = models.CharField(
        max_length=500, blank=False, null=False)
    significado_pib = models.CharField(max_length=400, blank=False, null=False)

    def __str__(self):
        return '{}/{}'.format(self.id_significado, self.abreviatura, self.significado_completo, self.significado_pib)


class Historico_pib(models.Model):
    id_pib_historico = models.AutoField(primary_key=True)
    lista_notam = models.CharField(max_length=20000)
    fecha_modificado = models.DateTimeField(
        default=datetime.now, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.fecha_modificado)

    class Meta:
        ordering = ('fecha_modificado',)



class Direccion_amhs(models.Model):
    direccionamiento = models.CharField(max_length=8, primary_key=True)
    def __str__(self):
        return '{}'.format(self.direccionamiento)

    class Meta:
        ordering = ('direccionamiento',)

class Prioridad(models.Model):
    prioridad = models.CharField(max_length=2, primary_key=True)
    def __str__(self):
        return '{}'.format(self.prioridad)

    class Meta:
        ordering = ('prioridad',)

class Tipo_notam(models.Model):
    tipo_notam = models.CharField(max_length=6, primary_key=True)
    def __str__(self):
        return '{}'.format(self.tipo_notam)

    class Meta:
        ordering = ('tipo_notam',)

class Serie_notam(models.Model):
    serie_notam = models.CharField(max_length=1, primary_key=True)
    descripcion = models.CharField(max_length=30)
    def __str__(self):
        return '{}'.format(self.serie_notam)

    class Meta:
        ordering = ('serie_notam',)



class Banco_notam_charly(models.Model):
    id_datanotam = models.AutoField(primary_key=True)

    indicador_prioridad = models.ForeignKey(Prioridad, on_delete=models.PROTECT, blank=False, null=False)
    direccion = models.ManyToManyField(Direccion_amhs)
    fecha_hora_deposito = models.CharField(max_length=10)
    indicador_remitente = models.CharField(max_length=8)

    serie = models.ForeignKey(Serie_notam, on_delete=models.PROTECT, blank=False, null=False)
    correlativo = models.CharField(max_length=7)

    tipo_notam = models.ForeignKey(Tipo_notam, on_delete=models.PROTECT, blank=False, null=False)

    referencia_notam = models.CharField(max_length=8)

    fir = models.CharField(max_length=4)

    codigo_notam_asunto = models.ForeignKey(Asunto, on_delete=models.PROTECT, blank=False, null=False)
    codigo_notam_estado = models.ForeignKey(Estado_asunto, on_delete=models.PROTECT, blank=False, null=False)

    transito = models.CharField(max_length=2)
    objetivo = models.CharField(max_length=3)
    alcance = models.CharField(max_length=2)
    limite_inferior = models.CharField(max_length=3, blank=True)
    limite_superior = models.CharField(max_length=3, blank=True)
    coordenadas = models.CharField(max_length=14, blank=True)
    lugar = models.ForeignKey(Aeropuerto, on_delete=models.PROTECT, blank=False, null=False)

    desde = models.CharField(max_length=10)
    hasta = models.CharField(max_length=10, blank=True)
    est = models.BooleanField(default=False)
    perm = models.BooleanField(default=False)
    horario = models.CharField(max_length=35, blank=True)
    texto_notam = models.CharField(max_length=800)
    limite_inferior_casilla = models.CharField(max_length=300, blank=True)
    limite_superior_casilla = models.CharField(max_length=300, blank=True)
    firma = models.CharField(max_length=20, blank=True)

    espaniol_decodificado = models.CharField(max_length=1000)
    ingresado = models.DateTimeField(default=datetime.now, blank=False, null=False)

    def __str__(self):
        return '{} {} - {}'.format(self.correlativo,self.tipo_notam, self.ingresado)

    class Meta:
        ordering = ('-correlativo','ingresado')



#############
#############

class Notam_trafico_charly_repla(models.Model):
    id_mensaje_c_r = models.CharField(max_length=8,primary_key=True)
    aftn1 = models.CharField(max_length=120)
    aftn2 = models.CharField(max_length=15)
    idnotam = models.CharField(max_length=85)
    resumen = models.CharField(max_length=65) #Q
    aplica_a = models.CharField(max_length=15) #A
    valido_desde = models.CharField(max_length=20) #B
    valido_hasta = models.CharField(max_length=20) #C
    mensaje = models.CharField(max_length=1200)
    es_pib = models.BooleanField(default=True)

    perm = models.BooleanField(default=False)
    est = models.BooleanField(default=False)

    asunto = models.CharField(max_length=100)
    estado_asunto = models.CharField(max_length=500)

    pib_publicar = models.CharField(max_length=1000)
    
    antecedente = models.CharField(max_length=2000, default='')

    form_oaci = models.FileField(upload_to='documents-%Y-%m-%d/', blank=True, null=True)

    ingresado = models.DateTimeField(default=datetime.now, blank=True, null=True)
    def __str__(self):
        return '{}'.format(self.idnotam)
    class Meta:
        ordering = ['idnotam', '-ingresado']
class Notam_trafico_charly_cancel(models.Model):
    id_mensaje_c_c = models.CharField(max_length=8,primary_key=True)
    aftn1 = models.CharField(max_length=120)
    aftn2 = models.CharField(max_length=15)
    idnotam = models.CharField(max_length=85)
    resumen = models.CharField(max_length=65) #Q
    aplica_a = models.CharField(max_length=15) #A
    valido_desde = models.CharField(max_length=20) #B
    valido_hasta = models.CharField(max_length=20) #C
    mensaje = models.CharField(max_length=1200)

    asunto = models.CharField(max_length=100)
    estado_asunto = models.CharField(max_length=500)

    antecedente = models.CharField(max_length=2000, default='')
    
    form_oaci = models.FileField(upload_to='documents-%Y-%m-%d/', blank=True, null=True)

    ingresado = models.DateTimeField(default=datetime.now, blank=True, null=True)
    def __str__(self):
        return '{}'.format(self.idnotam)
    class Meta:
        ordering = ['idnotam', '-ingresado']
class Notam_trafico_charly_new(models.Model):
    id_mensaje_c_n = models.CharField(max_length=8,primary_key=True)
    aftn1 = models.CharField(max_length=120)
    aftn2 = models.CharField(max_length=15)
    idnotam = models.CharField(max_length=85)
    resumen = models.CharField(max_length=65) #Q
    aplica_a = models.CharField(max_length=15) #A
    valido_desde = models.CharField(max_length=20) #B
    valido_hasta = models.CharField(max_length=20) #C
    mensaje = models.CharField(max_length=1200)
    es_pib = models.BooleanField(default=False)

    perm = models.BooleanField(default=False)
    est = models.BooleanField(default=False)

    asunto = models.CharField(max_length=100)
    estado_asunto = models.CharField(max_length=500)

    pib_publicar = models.CharField(max_length=1000)

    antecedente = models.CharField(max_length=2000, default='')

    form_oaci = models.FileField(upload_to='documents-%Y-%m-%d/', blank=True, null=True)

    ingresado = models.DateTimeField(default=datetime.now, blank=True, null=True)
    
    def __str__(self):
        return '{}'.format(self.idnotam)
    class Meta:
        ordering = ['idnotam', '-ingresado']
#############
#############
class Notam_trafico_alfa_repla(models.Model):
    id_mensaje_a_r = models.CharField(max_length=8,primary_key=True)
    aftn1 = models.CharField(max_length=120)
    aftn2 = models.CharField(max_length=15)
    idnotam = models.CharField(max_length=85)
    resumen = models.CharField(max_length=65) #Q
    aplica_a = models.CharField(max_length=15) #A
    valido_desde = models.CharField(max_length=20) #B
    valido_hasta = models.CharField(max_length=20) #C
    mensaje = models.CharField(max_length=1200)

    perm = models.BooleanField(default=False)
    est = models.BooleanField(default=False)

    asunto = models.CharField(max_length=100)
    estado_asunto = models.CharField(max_length=1000)

    antecedente = models.CharField(max_length=2000, default='')
    
    form_oaci = models.FileField(upload_to='documents-%Y-%m-%d/', blank=True, null=True)

    ingresado = models.DateTimeField(default=datetime.now, blank=True, null=True)
    def __str__(self):
        return '{}'.format(self.idnotam)
    class Meta:
        ordering = ['idnotam']
class Notam_trafico_alfa_cancel(models.Model):
    id_mensaje_a_c = models.CharField(max_length=8,primary_key=True)
    aftn1 = models.CharField(max_length=120)
    aftn2 = models.CharField(max_length=15)
    idnotam = models.CharField(max_length=85)
    resumen = models.CharField(max_length=65) #Q
    aplica_a = models.CharField(max_length=15) #A
    valido_desde = models.CharField(max_length=20) #B
    valido_hasta = models.CharField(max_length=20) #C
    mensaje = models.CharField(max_length=1200)

    asunto = models.CharField(max_length=100)
    estado_asunto = models.CharField(max_length=500)

    antecedente = models.CharField(max_length=2000, default='')
    
    form_oaci = models.FileField(upload_to='documents-%Y-%m-%d/', blank=True, null=True)

    ingresado = models.DateTimeField(default=datetime.now, blank=True, null=True)
    def __str__(self):
        return '{}'.format(self.idnotam)
class Notam_trafico_alfa_new(models.Model):
    class Meta:
        ordering = ['idnotam']
    id_mensaje_a_n = models.CharField(max_length=8,primary_key=True)
    aftn1 = models.CharField(max_length=120)
    aftn2 = models.CharField(max_length=15)
    idnotam = models.CharField(max_length=85)
    resumen = models.CharField(max_length=65) #Q
    aplica_a = models.CharField(max_length=15) #A
    valido_desde = models.CharField(max_length=20) #B
    valido_hasta = models.CharField(max_length=20) #C
    mensaje = models.CharField(max_length=1200)

    perm = models.BooleanField(default=False)
    est = models.BooleanField(default=False)

    asunto = models.CharField(max_length=100)
    estado_asunto = models.CharField(max_length=1000)

    antecedente = models.CharField(max_length=2000, default='')

    form_oaci = models.FileField(upload_to='documents-%Y-%m-%d/', blank=True, null=True)

    ingresado = models.DateTimeField(default=datetime.now, blank=True, null=True)
    
    def __str__(self):
        return '{}'.format(self.idnotam)
    class Meta:
        ordering = ['idnotam']




#class Banco_notam_alfa(models.Model):

    ################################# DESCRIPTION ####################################

    # full_text        # The full text of the NOTAM (for example, when constructed with from_str(s),
    #                            #  this will contain s.
    # notam_id         # The series and number/year of this NOTAM.
    # notam_type       # The NOTAM type: 'NEW', 'REPLACE', or 'CANCEL'.
    # ref_notam_id     # If this  NOTAM references a previous NOTAM (notam_type is 'REPLACE' or 'CANCEL'),
    #                            #  the series and number/year of the other NOTAM.
    # fir              # The FIR within which the subject of the information is located.
    # notam_code       # The five-letter NOTAM code, beginning with 'Q'. (Currently a simple str; at some
    #                            #  point may be further parsed to specify the code's meaning.)
    # traffic_type     # Set of affected traffic. Will contain one or more of:
    #                            #  'IFR'/'VFR'/'CHECKLIST'.
    # purpose          # Set of NOTAM purposes. Will contain one or more of:
    #                            #  'IMMEDIATE ATTENTION'/'OPERATIONAL SIGNIFICANCE'/'FLIGHT OPERATIONS'/
    #                            #  'MISC'/'CHECKLIST'.
    # scope            # Set of NOTAM scopes. Will contain one or more of:
    #                            #  'AERODROME'/'EN-ROUTE'/'NAV WARNING'/'CHECKLIST'.
    # fl_lower         # Lower vertical limit of NOTAM area of influence, expressed in flight levels (int).
    # fl_upper         # Upper vertical limit of NOTAM area of influence, expressed in flight levels (int).
    # area             # Approximate circle whose radius encompasses the NOTAM's whole area of influence.
    #                            #   This is a dict with keys: 'lat', 'long', 'radius' (str, str, int respectively).
    # location         # List of one or more ICAO location indicators, specifying the aerodrome or FIR
    #                            #  in which the facility, airspace, or condition being reported on is located.
    # valid_from       # The date and time at which the NOTAM comes into force (datetime.datetime).
    # valid_till       # For anything except a 'CANCEL'-type NOTAM, a date and time indicating duration of
    #                 #  information (datetime.datetime). If permanent, equal to datetime.datetime.max.
    #                 #  If the validity period is estimated, an instance of timeutils.EstimatedDateTime
    #                 #  with an attribute 'is_estimated' set to True.
    # schedule         # If the condition is active in accordance with a specific time date schedule, an
    #                 #  abbreviated textual description of this schedule.
    # body             # Text of NOTAM; Plain-language Entry (using ICAO Abbreviations).
    # limit_lower      # Textual specification of lower height limit of activities or restrictions.
    # limit_upper      # Textual specification of upper height limits of activities or restrictions.
    #
    # The following contain [start,end) indices for their corresponding NOTAM items (if such exist).
    # They can be used to index into Notam.full_text.
    # indices_item_a
    # indices_item_b
    # indices_item_c
    # indices_item_d
    # indices_item_e
    # indices_item_f
    # indices_item_g

