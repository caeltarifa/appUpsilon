
from django.db import models
from datetime import datetime

from apps.plan_vuelo.models import  Notam_trafico, Trabajador

# Create your models here.



class Pib_trafico(models.Model):
    ref_notam_amhs = models.OneToOneField(
        Notam_trafico,
        #related_name='xxxx',
        on_delete=models.PROTECT,
        primary_key=True,
    )

    oficialaro = models.ForeignKey(Trabajador,on_delete=models.PROTECT, blank=True, null=False) 
    
    decodificado = models.CharField(max_length=600)

    publicado = models.DateTimeField(blank=True, null=True)
    vigente = models.BooleanField(default=False)
    archivado = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.ref_notam_amhs
    class Meta:
        ordering = ['ref_notam_amhs']


class Pib_extenso(models.Model):
    notam_extenso = models.OneToOneField(
        Pib_trafico,
        #related_name='xxxx',
        on_delete=models.PROTECT,
        primary_key=True,
    )

    notam_id = models.CharField(max_length=10)     ##    notam_id   A3465/19              <class 'str'>
    notam_tipo = models.CharField(max_length=10)     ##    notam_type   NEW              <class 'str'>
    ref_notam_id = models.CharField(max_length=10)     ##    ref_notam_id   None              <class 'NoneType'>
    fir = models.CharField(max_length=10)     ##    fir   SPIM              <class 'str'>
    notam_codigo = models.CharField(max_length=10)     ##    notam_code   QRALW              <class 'str'>
    tipo_trafico = models.CharField(max_length=50)     ##    traffic_type   {'IFR', 'VFR'}              <class 'set'>
    
    proposito = models.CharField(max_length=200)     ##    purpose   {'OPERATIONAL SIGNIFICANCE', 'FLIGHT OPERATIONS', 'IMMEDIATE ATTENTION'}              <class 'set'>
    alcance = models.CharField(max_length=100)       ##    scope   {'NAV WARNING'}              <class 'set'>
    
    fl_inferior = models.IntegerField()     ##    fl_lower   0              <class 'int'>
    fl_superior = models.IntegerField()     ##    fl_upper   30              <class 'int'>
    
    area = models.CharField(max_length=100)     ##    area   {'lat': '1218S', 'long': '07654W', 'radius': 0}              <class 'dict'>
    
    lugar = models.CharField(max_length=50)     ##    location   ['SPJC']              <class 'list'>
    valid_desde = models.DateTimeField(blank=True, null=True)     ##    valid_from   2019-07-25 13:30:00+00:00      <class 'datetime.datetime'>
    valid_hasta = models.DateTimeField(blank=True, null=True)     ##    valid_till   2019-07-29 20:00:00+00:00      <class 'datetime.datetime'>
    agendado = models.CharField(max_length=150)     ##    schedule   DAYS 25,26,27 AND 29 BTN 1330-2000              <class 'str'>
    
    cuerpo =  models.CharField(max_length=400)     ##    body   AIR PARADE DUE TO PERUVIAN INDEPENDENCE DAY. RPAS/DRONES/PARAGLIDERS AND SPORTS ACTIVITIES ARE PROHIBITED. ALL FLT HAVE TO AVOID OVERFLY. PREVIOUS COOR BTN LAS PALMAS TWR AND ACC LIMA IS REQUIRED. COORD: 121806S0765410W 121230S0770340W 120605S077044W 120332S0770238W 120457S0765829W              <class 'str'>
    
    limit_superior = models.CharField(max_length=10)     ##    limit_lower   GND              <class 'str'>
    limit_inferior = models.CharField(max_length=10)     ##    limit_upper   3000FT              <class 'str'>
    indices_item_a = models.CharField(max_length=15)     ##    indices_item_a   (66, 70)              <class 'tuple'>
    indices_item_b = models.CharField(max_length=15)     ##    indices_item_b   (75, 85)              <class 'tuple'>
    indices_item_c = models.CharField(max_length=15)     ##    indices_item_c   (89, 99)              <class 'tuple'>
    indices_item_d = models.CharField(max_length=15)     ##    indices_item_d   (103, 137)              <class 'tuple'>
    indices_item_e = models.CharField(max_length=15)     ##    indices_item_e   (141, 423)              <class 'tuple'>
    indices_item_f = models.CharField(max_length=15)     ##    indices_item_f   (427, 430)              <class 'tuple'>
    indices_item_g = models.CharField(max_length=15)     ##    indices_item_g   (434, 440)              <class 'tuple'>
    def __unicode__(self):
        return self.notam_id
    class Meta:
        ordering = ['notam_id']



    ################################# DESCRIPTION ####################################

    #full_text        # The full text of the NOTAM (for example, when constructed with from_str(s),
    #                            #  this will contain s.
    #notam_id         # The series and number/year of this NOTAM.
    #notam_type       # The NOTAM type: 'NEW', 'REPLACE', or 'CANCEL'.
    #ref_notam_id     # If this  NOTAM references a previous NOTAM (notam_type is 'REPLACE' or 'CANCEL'),
    #                            #  the series and number/year of the other NOTAM.
    #fir              # The FIR within which the subject of the information is located.
    #notam_code       # The five-letter NOTAM code, beginning with 'Q'. (Currently a simple str; at some
    #                            #  point may be further parsed to specify the code's meaning.)
    #traffic_type     # Set of affected traffic. Will contain one or more of:
    #                            #  'IFR'/'VFR'/'CHECKLIST'.
    #purpose          # Set of NOTAM purposes. Will contain one or more of:
    #                            #  'IMMEDIATE ATTENTION'/'OPERATIONAL SIGNIFICANCE'/'FLIGHT OPERATIONS'/
    #                            #  'MISC'/'CHECKLIST'.
    #scope            # Set of NOTAM scopes. Will contain one or more of:
    #                            #  'AERODROME'/'EN-ROUTE'/'NAV WARNING'/'CHECKLIST'.
    #fl_lower         # Lower vertical limit of NOTAM area of influence, expressed in flight levels (int).
    #fl_upper         # Upper vertical limit of NOTAM area of influence, expressed in flight levels (int).
    #area             # Approximate circle whose radius encompasses the NOTAM's whole area of influence.
    #                            #   This is a dict with keys: 'lat', 'long', 'radius' (str, str, int respectively).
    #location         # List of one or more ICAO location indicators, specifying the aerodrome or FIR
    #                            #  in which the facility, airspace, or condition being reported on is located.
    #valid_from       # The date and time at which the NOTAM comes into force (datetime.datetime).
    #valid_till       # For anything except a 'CANCEL'-type NOTAM, a date and time indicating duration of
    #                 #  information (datetime.datetime). If permanent, equal to datetime.datetime.max.
    #                 #  If the validity period is estimated, an instance of timeutils.EstimatedDateTime
    #                 #  with an attribute 'is_estimated' set to True.
    #schedule         # If the condition is active in accordance with a specific time date schedule, an
    #                 #  abbreviated textual description of this schedule.
    #body             # Text of NOTAM; Plain-language Entry (using ICAO Abbreviations).
    #limit_lower      # Textual specification of lower height limit of activities or restrictions.
    #limit_upper      # Textual specification of upper height limits of activities or restrictions.
    #
    ## The following contain [start,end) indices for their corresponding NOTAM items (if such exist).
    ## They can be used to index into Notam.full_text.
    #indices_item_a 
    #indices_item_b 
    #indices_item_c 
    #indices_item_d 
    #indices_item_e 
    #indices_item_f 
    #indices_item_g