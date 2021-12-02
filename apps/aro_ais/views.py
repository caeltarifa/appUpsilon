from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import connection
from django.contrib.auth.models import Group
import datetime
import json



##IMPORTANDO MODELOS DE BANCO DE DATOS NOTAM 
from apps.aro_ais.models import Notam_trafico_charly_repla as Banco_charly_repla
from apps.aro_ais.models import Notam_trafico_charly_cancel as Banco_charly_cancel
from apps.aro_ais.models import Notam_trafico_charly_new as Banco_charly_new
#######
#######
from apps.aro_ais.models import Notam_trafico_alfa_repla as Banco_alfa_repla
from apps.aro_ais.models import Notam_trafico_alfa_cancel as Banco_alfa_cancel
from apps.aro_ais.models import Notam_trafico_alfa_new as Banco_alfa_new



##IMPORTANDO MODELO DEL BANCO DE DATOS AMHS 
from apps.plan_vuelo.models import Notam_trafico_charly_cancel as Amhs_charly_cancel
from apps.plan_vuelo.models import Notam_trafico_charly_repla as Amhs_charly_repla
from apps.plan_vuelo.models import Notam_trafico_charly_new as Amhs_charly_new
###########
###########
from apps.plan_vuelo.models import Notam_trafico_alfa_repla as Amhs_alfa_repla
from apps.plan_vuelo.models import Notam_trafico_alfa_cancel as Amhs_alfa_cancel
from apps.plan_vuelo.models import Notam_trafico_alfa_new as Amhs_alfa_new



from appUpsilon.views import estadisticas_charly_new,estadisticas_alfa_new, estadisticas_charly_repla, estadisticas_alfa_repla
# Create your views here.


from apps.plan_vuelo.models import  Notam_trafico, Trabajador, Aeropuerto
from apps.aro_ais.models import  Pib_trafico, Pib_extenso, Pib_registro_documento
from apps.aro_ais.models import Abreviatura_8400

from apps.aro_ais.models import  Letra_asunto,Asunto,Estado_asunto

#from apps.aro_ais.models import  Simbolo_8400, Abreviatura_8400



from apps.trabajadoresATS.models import TrabajadoresATS, CuentasATS

from django.contrib.auth.decorators import login_required

#LIBRARY FOR CAST "['A','B','C']" TO  ['A','B','C'] (list element)
import ast
# Create your views here.

###########################################################################
##### APP CLASIFICACION DE USUARIOS
###########################################################################

def view_panel_aroaislp(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AISNACIONAL').exists():
        #equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        return render(request, 'temp_plan_vuelo/temp_aro_ais/index_aroais.html')# ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
    else:
        return redirect('login')

def view_panel_notaminternacional(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AISNACIONAL').exists():
        return render(request, 'temp_plan_vuelo/temp_aro_ais/index_notaminternacional.html')
    else:
        return redirect('login')


def view_ais_for_aed(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AISNACIONAL').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        return render(request, 'temp_plan_vuelo/temp_aro_ais/index_ais_for_aed.html' ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
    else:
        return redirect('login')


def view_ais_for_person(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AISNACIONAL').exists():
        return render(request, 'temp_plan_vuelo/temp_aro_ais/index_ais_for_aed.html' ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
    else:
        return redirect('login')


def view_admin_ais(request):
    if request.user.is_authenticated:
        trabajadores= TrabajadoresATS.objects.using('aasana_bd').raw("select * from trabajadores limit 5 ")
        cuentas= CuentasATS.objects.using('aasana_bd').raw("select * from cuentas limit 5 ")
        respuesta= CuentasATS.objects.using('aasana_bd').raw("select id_cuenta, password, usuario from cuentas where id_cuenta=1 ")[0]
        respuesta=respuesta.usuario + '----'+ respuesta.password
        return render(request, 'temp_plan_vuelo/aroais.html', {'trabajadores':trabajadores, 'cuentas':cuentas, 'respuesta':respuesta} )
    else:
        return redirect('login')




###########################################################################
##### APP CREADOR DE NOTAM N R C, SERIE ALPHA Y CHARLIE
###########################################################################

def view_new_notam(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AISNACIONAL').exists():
        lista_letras = Letra_asunto.objects.all().order_by('id_letra')

        lista_georeferencias = Aeropuerto.objects.raw( "(select aeropuerto, icao, fuente, geo_arp AS georef   from plan_vuelo_aeropuerto  inner join (VALUES ('ARP')) AS t (fuente)  on geo_arp not like %(nil)s and aeropuerto <> 39)  union  (select aeropuerto, icao, fuente, geo_vor AS georef  from plan_vuelo_aeropuerto  inner join (VALUES ('VOR')) AS t (fuente)  on geo_vor not like %(nil)s)   union  (select aeropuerto, icao, fuente, geo_ils AS georef  from plan_vuelo_aeropuerto  inner join (VALUES ('ILS')) AS t (fuente)  on geo_ils not like %(nil)s)   union  (select aeropuerto, icao, fuente, geo_ils_gp_dme AS georef  from plan_vuelo_aeropuerto  inner join (VALUES ('ILS_GP_DME')) AS t (fuente)  on geo_ils_gp_dme not like %(nil)s)  union  (select aeropuerto, icao, fuente, geo_l AS georef  from plan_vuelo_aeropuerto  inner join (VALUES ('L')) AS t (fuente)  on geo_l not like %(nil)s)   union  (select aeropuerto, icao, fuente, ils_llz AS georef from plan_vuelo_aeropuerto  inner join (VALUES ('ILS_LLZ')) AS t (fuente)  on ils_llz not like %(nil)s) union (select aeropuerto, icao, fuente, ils_loc AS georef from plan_vuelo_aeropuerto  inner join (VALUES ('ILS_LOC')) AS t (fuente)  on ils_loc not like %(nil)s) union (select aeropuerto, icao, fuente, dvor_dme AS georef from plan_vuelo_aeropuerto  inner join (VALUES ('DVOR_DME')) AS t (fuente)  on dvor_dme  not like %(nil)s)   union  (select aeropuerto, icao, fuente, geo_mm AS georef  from plan_vuelo_aeropuerto  inner join (VALUES ('MM')) AS t (fuente)  on geo_mm not like %(nil)s)   union  (select aeropuerto, icao, fuente, geo_ndb AS georef  from plan_vuelo_aeropuerto  inner join (VALUES ('NDB')) AS t (fuente)  on geo_ndb not like %(nil)s)   union  (select aeropuerto, icao, iata AS fuente, geo_arp AS georef  from plan_vuelo_aeropuerto  where iata like 'SLLF')  order by icao asc, fuente asc" , { 'nil' : "NIL"} )

        for geo in lista_georeferencias:
            if 'SLLF' in geo.fuente:
                aux=geo.fuente
                geo.fuente = geo.icao
                geo.icao = aux
            part1 = str(geo.georef.split('S')[0])[0:4]
            part2 = str(geo.georef.split('S')[1])[0:5]

            geo.georef = part1 + 'S' + part2 + 'W'

        return render(request, 'temp_plan_vuelo/temp_aro_ais/new_notam.html', {'lista_georeferencias': lista_georeferencias, 'lista_letras': lista_letras})
    else:
        return redirect('login')

def view_new_notam_2(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AISNACIONAL').exists():
        lista_letras = Letra_asunto.objects.all().order_by('id_letra')

        lista_georeferencias = Aeropuerto.objects.raw( "(select aeropuerto, icao, fuente, geo_arp AS georef   from plan_vuelo_aeropuerto  inner join (VALUES ('ARP')) AS t (fuente)  on geo_arp not like %(nil)s and aeropuerto <> 39)  union  (select aeropuerto, icao, fuente, geo_vor AS georef  from plan_vuelo_aeropuerto  inner join (VALUES ('VOR')) AS t (fuente)  on geo_vor not like %(nil)s)   union  (select aeropuerto, icao, fuente, geo_ils AS georef  from plan_vuelo_aeropuerto  inner join (VALUES ('ILS')) AS t (fuente)  on geo_ils not like %(nil)s)   union  (select aeropuerto, icao, fuente, geo_ils_gp_dme AS georef  from plan_vuelo_aeropuerto  inner join (VALUES ('ILS_GP_DME')) AS t (fuente)  on geo_ils_gp_dme not like %(nil)s)  union  (select aeropuerto, icao, fuente, geo_l AS georef  from plan_vuelo_aeropuerto  inner join (VALUES ('L')) AS t (fuente)  on geo_l not like %(nil)s)   union  (select aeropuerto, icao, fuente, ils_llz AS georef from plan_vuelo_aeropuerto  inner join (VALUES ('ILS_LLZ')) AS t (fuente)  on ils_llz not like %(nil)s) union (select aeropuerto, icao, fuente, ils_loc AS georef from plan_vuelo_aeropuerto  inner join (VALUES ('ILS_LOC')) AS t (fuente)  on ils_loc not like %(nil)s) union (select aeropuerto, icao, fuente, dvor_dme AS georef from plan_vuelo_aeropuerto  inner join (VALUES ('DVOR_DME')) AS t (fuente)  on dvor_dme  not like %(nil)s)   union  (select aeropuerto, icao, fuente, geo_mm AS georef  from plan_vuelo_aeropuerto  inner join (VALUES ('MM')) AS t (fuente)  on geo_mm not like %(nil)s)   union  (select aeropuerto, icao, fuente, geo_ndb AS georef  from plan_vuelo_aeropuerto  inner join (VALUES ('NDB')) AS t (fuente)  on geo_ndb not like %(nil)s)   union  (select aeropuerto, icao, iata AS fuente, geo_arp AS georef  from plan_vuelo_aeropuerto  where iata like 'SLLF')  order by icao asc, fuente asc" , { 'nil' : "NIL"} )

        for geo in lista_georeferencias:
            if 'SLLF' in geo.fuente:
                aux=geo.fuente
                geo.fuente = geo.icao
                geo.icao = aux
            part1 = str(geo.georef.split('S')[0])[0:4]
            part2 = str(geo.georef.split('S')[1])[0:5]

            geo.georef = part1 + 'S' + part2 + 'W'

        return render(request, 'temp_plan_vuelo/temp_aro_ais/new_notam_2.html', {'lista_georeferencias': lista_georeferencias, 'lista_letras': lista_letras})
    else:
        return redirect('login')
###########################################################################
##### APP MANUAL DE PARA LOS SERVICIOS DE INFORMACION AERONAUTICA DOC 8126
###########################################################################
def view_getAsunto(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AISNACIONAL').exists():
        letra = str(request.GET.dict()['letra'])
        asunto = Asunto.objects.filter(letra_asunto_id=letra)
        vec_asuntos = [x.id_asunto for x in asunto]
        return JsonResponse({'vec_asunto':vec_asuntos}, status=200)
    else:
        return redirect('login')

def view_getEstadoAsunto(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AISNACIONAL').exists():
        asunto = str(request.GET.dict()['asunto'])
        
        estado_asunto = Estado_asunto.objects.filter(id_asunto__id_asunto=asunto)
        vec_estado_asuntos = [x.id_estado_asunto for x in estado_asunto]
        return JsonResponse({'vec_estado_asunto':vec_estado_asuntos, 'asunto_fraseologia': "asunto para cuerpo E)", 'asunto_espaniol': "asunto espaniol PIB", }, status=200)
    else:
        return redirect('login')

def view_codigos_abreviaturas(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AISNACIONAL').exists():
        
        lista_letras = Letra_asunto.objects.all().order_by('id_letra')
        return render(request, 'temp_plan_vuelo/temp_aro_ais/diccionario_aeronautico.html', {'lista_letras':lista_letras} )
    else:
        return redirect('login')













def view_pib_automatizado(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AROAISLP').exists():

        lista_pib_pendiente = Pib_trafico.objects.raw("select * from ( select * from aro_ais_pib_trafico inner join aro_ais_pib_extenso on ref_notam_amhs_id = notam_extenso_id and pendiente='t' and (notam_id like %(notamC)s and notam_id not like %(notamA)s )) as pib inner join plan_vuelo_notam_trafico on id_mensaje=ref_notam_amhs_id order by DATE(ingresado) desc;", {'notamC':'%C%/2%', 'notamA':'(A%'})
        lista_pib_archivado = Pib_trafico.objects.raw("select * from aro_ais_pib_trafico inner join aro_ais_pib_extenso on ref_notam_amhs_id = notam_extenso_id and archivado='t'  ")
        lista_pib_publicado = Pib_trafico.objects.raw("select * from aro_ais_pib_trafico inner join aro_ais_pib_extenso on ref_notam_amhs_id = notam_extenso_id and vigente='t' and msj_publicado!=''  ")
        lista_notams_recientes=Notam_trafico.objects.all().order_by('-ingresado')[:25]

        # ref_notam_amhs_id | decodificado | publicado | vigente | archivado | oficialaro_id | pendiente   | msj_publicado | Instalacion  | notam_extenso_id    | notam_id |
        # notam_tipo | ref_notam_id | fir  | notam_codigo |  tipo_trafico  | proposito |    alcance    | fl_inferior | fl_superior | area |  
        # lugar   |      valid_desde       |      valid_hasta       |   agendado    | cuerpo | limit_superior | limit_inferior | indices_item_a |
        # indices_item_b | indices_item_c | indices_item_d | indices_item_e | indices_item_f | indices_item_g
        lista_pib_pendiente=[serializar_pibtrafico_pibextenso(pib) for pib in lista_pib_pendiente]
        lista_pib_archivado=[serializar_pibtrafico_pibextenso(pib) for pib in lista_pib_archivado]
        lista_pib_publicado=[serializar_pibtrafico_pibextenso(pib) for pib in lista_pib_publicado]
        lista_notams_recientes=[serializar_notam(notamx) for notamx in lista_notams_recientes]
        
        return render(request, 'temp_plan_vuelo/temp_aro_ais/notam_automatizado.html' ,{'lista_pendiente':lista_pib_pendiente, 'lista_archivado':lista_pib_archivado, 'lista_publicado':lista_pib_publicado, 'lista_notam':lista_notams_recientes} )
    else:
        return redirect('login')


def view_imprimir_pibrealtime(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='TODOS_SERVICIOS').exists():
        pib_vigente = Pib_trafico.objects.raw("select * from (select ref_notam_amhs_id, lugar, instalacion, msj_publicado from aro_ais_pib_trafico inner join aro_ais_pib_extenso on ref_notam_amhs_id = notam_extenso_id and vigente='t' and msj_publicado!='') as pib inner join plan_vuelo_aeropuerto on icao like substring(lugar, 3, 4) order by lugar asc ")
        
        pib_vigente = [{'ref_notam_amhs_id':pib.ref_notam_amhs_id,'nombre': pib.nombre,'lugar':str(pib.lugar)[2:6], 'instalacion':pib.instalacion, 'msj_publicado':pib.msj_publicado} for pib in pib_vigente]
        
        return render(request, 'temp_plan_vuelo/temp_aro_ais/print_notam_realtime.html' ,{'pib_vigente':pib_vigente} )
    else:
        return redirect('login')


def view_todos_notams(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='TODOS_SERVICIOS').exists():
        lista_notams_recientes=Notam_trafico.objects.all().order_by('-ingresado')[:100]

        
        charly_recientes_new = Amhs_charly_new.objects.extra(select={'id_mensaje':'id_mensaje_c_n'}).all().order_by('-ingresado')[:50]
        charly_recientes_new = [ serializar_notam(notam) for notam in charly_recientes_new]
        charly_recientes_repla = Amhs_charly_repla.objects.extra(select={'id_mensaje':'id_mensaje_c_r'}).all().order_by('-ingresado')[:50]
        charly_recientes_repla = [ serializar_notam(notam) for notam in charly_recientes_repla]
        charly_recientes_cancel = Amhs_charly_cancel.objects.extra(select={'id_mensaje':'id_mensaje_c_c'}).all().order_by('-ingresado')[:50]
        charly_recientes_cancel = [ serializar_notam(notam) for notam in charly_recientes_cancel]
        
        
        alfa_recientes_new = Amhs_alfa_new.objects.extra(select={'id_mensaje':'id_mensaje_a_n'}).all().order_by('-ingresado')[:50]
        alfa_recientes_new = [serializar_notam(notam) for notam in alfa_recientes_new]
        alfa_recientes_repla = Amhs_alfa_repla.objects.extra(select={'id_mensaje':'id_mensaje_a_r'}).all().order_by('-ingresado')[:50]
        alfa_recientes_repla = [serializar_notam(notam) for notam in alfa_recientes_repla]
        alfa_recientes_cancel = Amhs_alfa_cancel.objects.extra(select={'id_mensaje':'id_mensaje_a_c'}).all().order_by('-ingresado')[:50]
        alfa_recientes_cancel = [serializar_notam(notam) for notam in alfa_recientes_cancel]
        #lista_notams_recientes=[serializar_notam(notamx) for notamx in lista_notams_recientes]

        

        lista_notam_charly = []
        lista_notam_alfa = []
        
        #for notam in lista_notams_recientes:
        #    if '(C' in notam.idnotam:
        #        lista_notam_charly.append(serializar_notam(notam))
        #    else:
        #        lista_notam_alfa.append(serializar_notam(notam))
        #return render(request, 'temp_plan_vuelo/temp_aro_ais/lista_notam.html' ,{'lista_notam_charly':lista_notam_charly, 'lista_notam_alfa':lista_notam_alfa} )
        return render(request, 'temp_plan_vuelo/temp_aro_ais/lista_notam.html' ,{'charly_recientes_new': charly_recientes_new, 'charly_recientes_repla':charly_recientes_repla,'charly_recientes_cancel':charly_recientes_cancel,'alfa_recientes_new': alfa_recientes_new, 'alfa_recientes_repla':alfa_recientes_repla,'alfa_recientes_cancel':alfa_recientes_cancel} )
    else:
        return redirect('login')

def serializar_notam(notamx):
    return {
        'id_mensaje': notamx.id_mensaje,
        'aftn1': notamx.aftn1,
        'aftn2': notamx.aftn2,
        'idnotam': notamx.idnotam,
        'resumen': notamx.resumen,
        'aplica_a': notamx.aplica_a,
        'valido_desde': notamx.valido_desde,
        'valido_hasta': notamx.valido_hasta,
        'mensaje': notamx.mensaje,
    }



###########################################################################
##### APP MUESTRA EL BANCO DE NOTAM CLASIFICADO EN CHARLIE Y ALPHA, DE LA FECHA DE HOY
###########################################################################
from itertools import chain
from operator import attrgetter
def view_banco_notam(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='TODOS_SERVICIOS').exists():
        #lista_notams_recientes=Notam_trafico.objects.all().order_by('-ingresado')[:100]


        #lista_notam_charly = Banco_charly_new.objects.extra(select={'id_mensaje':'id_mensaje_c_n'}).filter(ingresado__year=datetime.date.today().year, ingresado__month=datetime.date.today().month, ingresado__day=datetime.date.today().day).order_by('ingresado')
        lista_notam_charly = Banco_charly_new.objects.extra(select={'id_mensaje':'id_mensaje_c_n'}).all().exclude(id_mensaje_c_n__contains='/20').exclude(id_mensaje_c_n__contains='/19').exclude(id_mensaje_c_n__contains='/18').order_by('-id_mensaje_c_n')[:25]
            #lista_notam_charly = [ serializar_notam_banco_charly(notam) for notam in lista_notam_charly]
        
        #lista_notam_charly2 = Banco_charly_repla.objects.extra(select={'id_mensaje':'id_mensaje_c_r'}).filter(ingresado__year=datetime.date.today().year, ingresado__month=datetime.date.today().month, ingresado__day=datetime.date.today().day).order_by('ingresado')
        lista_notam_charly2 = Banco_charly_repla.objects.extra(select={'id_mensaje':'id_mensaje_c_r'}).all().exclude(id_mensaje_c_r__contains='/20').exclude(id_mensaje_c_r__contains='/19').exclude(id_mensaje_c_r__contains='/18').order_by('-id_mensaje_c_r')[:25]
            #lista_notam_charly2 = [ serializar_notam_banco_charly(notam) for notam in lista_notam_charly2]
        
        #lista_notam_charly3 = Banco_charly_cancel.objects.extra(select={'id_mensaje':'id_mensaje_c_c'}).filter(ingresado__year=datetime.date.today().year, ingresado__month=datetime.date.today().month, ingresado__day=datetime.date.today().day).order_by('ingresado')
        lista_notam_charly3 = Banco_charly_cancel.objects.extra(select={'id_mensaje':'id_mensaje_c_c'}).all().exclude(id_mensaje_c_c__contains='/20').exclude(id_mensaje_c_c__contains='/19').exclude( id_mensaje_c_c__contains='/18').order_by('-id_mensaje_c_c')[:25]
            #lista_notam_charly3 = [ serializar_notam_banco_charly(notam) for notam in lista_notam_charly3]
        

        #lista_notam_charly = chain(lista_notam_charly, lista_notam_charly2, lista_notam_charly3)
        lista_notam_charly = sorted(chain(lista_notam_charly, lista_notam_charly2, lista_notam_charly3), key=attrgetter('id_mensaje'), reverse=True)
        
        lista_notam_charly = [ serializar_notam_banco_charly(notam)  for notam in lista_notam_charly]
        for notam in lista_notam_charly:
            if not ('/21' in notam['idnotam']):
                lista_notam_charly.remove(notam)

        

        #lista_notam_charly += lista_notam_charly2 + lista_notam_charly3
        #-------------------------------------------------------------------------------------
        lista_notam_alfa = Banco_alfa_new.objects.extra(select={'id_mensaje':'id_mensaje_a_n'}).exclude(id_mensaje_a_n__contains='/20').exclude(id_mensaje_a_n__contains='/19').exclude(id_mensaje_a_n__contains='/18').filter(ingresado__year=datetime.date.today().year, ingresado__month=datetime.date.today().month, ingresado__day=datetime.date.today().day).order_by('-id_mensaje_a_n')
        #lista_notam_alfa = Banco_alfa_new.objects.extra(select={'id_mensaje':'id_mensaje_a_n'}).all().order_by('ingresado')[:25]
            #lista_notam_alfa = [ serializar_notam_banco_alfa(notam) for notam in lista_notam_alfa]
        
        lista_notam_alfa2 = Banco_alfa_repla.objects.extra(select={'id_mensaje':'id_mensaje_a_r'}).exclude(id_mensaje_a_r__contains='/20').exclude(id_mensaje_a_r__contains='/19').exclude(id_mensaje_a_r__contains='/18').filter(ingresado__year=datetime.date.today().year, ingresado__month=datetime.date.today().month, ingresado__day=datetime.date.today().day).order_by('-id_mensaje_a_r')
        #lista_notam_alfa2 = Banco_alfa_repla.objects.extra(select={'id_mensaje':'id_mensaje_a_r'}).all().order_by('ingresado')[:25]
            #lista_notam_alfa2 = [ serializar_notam_banco_alfa(notam) for notam in lista_notam_alfa2]
        
        lista_notam_alfa3 = Banco_alfa_cancel.objects.extra(select={'id_mensaje':'id_mensaje_a_c'}).exclude(id_mensaje_a_c__contains='/20').exclude(id_mensaje_a_c__contains='/19').exclude(id_mensaje_a_c__contains='/18').filter(ingresado__year=datetime.date.today().year, ingresado__month=datetime.date.today().month, ingresado__day=datetime.date.today().day).order_by('-id_mensaje_a_c')
        #lista_notam_alfa3 = Banco_alfa_cancel.objects.extra(select={'id_mensaje':'id_mensaje_a_c'}).all().order_by('ingresado')[:25]
            #lista_notam_alfa3 = [ serializar_notam_banco_alfa(notam) for notam in lista_notam_alfa3]

        lista_notam_alfa = sorted(chain(lista_notam_alfa, lista_notam_alfa2, lista_notam_alfa3), key=attrgetter('id_mensaje'), reverse=True)
        lista_notam_alfa = [ serializar_notam_banco_alfa(notam) for notam in lista_notam_alfa]
        for notam in lista_notam_alfa:
            if not ('/21' in notam['idnotam']):
                lista_notam_alfa.remove(notam)

        #lista_notam_alfa += lista_notam_alfa2 + lista_notam_alfa3

        return render(request, 'temp_plan_vuelo/temp_aro_ais/banco_notam.html',{'lista_notam_charly':lista_notam_charly, 'lista_notam_alfa':lista_notam_alfa} )
    else:
        return redirect('login')

def serializar_notam_banco_charly(notam):
    if notam.form_oaci:
        archivo = notam.form_oaci.url
    else:
        archivo = ""
    try:
        return {
            'titulo':'NOTAM CHARLIE',
            'aftn2': notam.aftn2,
            'id_mensaje': notam.id_mensaje,
            'idnotam': notam.idnotam,
            'resumen': notam.resumen,
            'aplica_a': notam.aplica_a,
            'valido_desde': notam.valido_desde,
            'valido_hasta': notam.valido_hasta,
            'mensaje': notam.mensaje+')',
            'es_pib': notam.es_pib,
            'asunto': notam.asunto,
            'estado_asunto': notam.estado_asunto,
            'pib_publicar': notam.pib_publicar,
            'antecedente': notam.antecedente,
            'form_oaci': archivo,
        }
    except:
        return {
            'titulo':'NOTAM CHARLIE',
            'id_mensaje': notam.id_mensaje,
            'idnotam': notam.idnotam,
            'resumen': notam.resumen,
            'aplica_a': notam.aplica_a,
            'valido_desde': notam.valido_desde,
            'valido_hasta': notam.valido_hasta,
            'mensaje': notam.mensaje+')',
            'asunto': notam.asunto,
            'estado_asunto': notam.estado_asunto,
            'antecedente': notam.antecedente,
            'form_oaci': archivo,
        }
    

def serializar_notam_banco_alfa(notam):
    if notam.form_oaci:
        archivo = notam.form_oaci.url
    else:
        archivo = ""
    return {
        'titulo':'NOTAM ALPHA',
        'id_mensaje': notam.id_mensaje,
        'idnotam': notam.idnotam,
        'resumen': notam.resumen,
        'aplica_a': notam.aplica_a,
        'valido_desde': notam.valido_desde,
        'valido_hasta': notam.valido_hasta,
        'mensaje': notam.mensaje,
        'asunto': notam.asunto,
        'estado_asunto': notam.estado_asunto,
        'antecedente': notam.antecedente,
        'form_oaci': archivo,
    }

def view_notam_modal_charly(request, id_notam):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='TODOS_SERVICIOS').exists():
        #id_notam = str(request.GET.get('id_notam'))
        id_notam = str(id_notam)
        
        if Banco_charly_new.objects.filter(id_mensaje_c_n=id_notam).exists():
            dato_notam = Banco_charly_new.objects.extra(select={'id_mensaje':'id_mensaje_c_n'}).get(id_mensaje_c_n=id_notam)
        if Banco_charly_repla.objects.filter(id_mensaje_c_r=id_notam).exists():
            dato_notam = Banco_charly_repla.objects.extra(select={'id_mensaje':'id_mensaje_c_r'}).get(id_mensaje_c_r=id_notam)
        if Banco_charly_cancel.objects.filter(id_mensaje_c_c=id_notam).exists():
            dato_notam = Banco_charly_cancel.objects.extra(select={'id_mensaje':'id_mensaje_c_c'}).get(id_mensaje_c_c=id_notam)

        dic={
                    'lat' : '1658S',  
                    'long' : '06508W',
                    'radius'    : 5
                }
        return render(request, 'temp_plan_vuelo/modal_mensaje_completo.html', {'data': serializar_notam_banco_charly(dato_notam), 'area':dic }  ) #retorno el modal y el contexto
        #return JsonResponse({'vec_estado_asunto':vec_estado_asuntos, 'asunto_fraseologia': "asunto para cuerpo E)", 'asunto_espaniol': "asunto espaniol PIB", }, status=200)
    else:
        return redirect('login')

def view_notam_modal_alfa(request, id_notam):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='TODOS_SERVICIOS').exists():
        #id_notam = str(request.GET.get('id_notam'))
        id_notam = str(id_notam)
        
        if Banco_alfa_new.objects.filter(id_mensaje_a_n=id_notam).exists():
            dato_notam = Banco_alfa_new.objects.extra(select={'id_mensaje':'id_mensaje_a_n'}).get(id_mensaje_a_n=id_notam)
        
        if Banco_alfa_repla.objects.filter(id_mensaje_a_r=id_notam).exists():
            dato_notam = Banco_alfa_repla.objects.extra(select={'id_mensaje':'id_mensaje_a_r'}).get(id_mensaje_a_r=id_notam)
        
        if Banco_alfa_cancel.objects.filter(id_mensaje_a_c=id_notam).exists():
            dato_notam = Banco_alfa_cancel.objects.extra(select={'id_mensaje':'id_mensaje_a_c'}).get(id_mensaje_a_c=id_notam)

        dic={
                    'lat' : '1658S',  
                    'long' : '06508W',
                    'radius'    : 5
                }
        return render(request, 'temp_plan_vuelo/modal_mensaje_completo.html', {'data': serializar_notam_banco_alfa(dato_notam), 'area':dic }  ) #retorno el modal y el contexto
        #return JsonResponse({'vec_estado_asunto':vec_estado_asuntos, 'asunto_fraseologia': "asunto para cuerpo E)", 'asunto_espaniol': "asunto espaniol PIB", }, status=200)
    else:
        return redirect('login')


###########################################################################
##### APP BUSCADOR DE NOTAMS SEGUN SERIE Y RANGO DE FECHAS
###########################################################################

def view_api_notam_search(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='TODOS_SERVICIOS').exists():
        # buscar notams
        get_inicio = str(request.GET.get('inicio'))
        get_fin = str(request.GET.get('fin'))
        get_tipo = str(request.GET.get('tipo'))
            
            
        lista_notam_charly=[]
        if 'charlie' in get_tipo:
            if get_inicio in get_fin:
                anio, mes, dia = get_inicio.split('-')

                lista_notam_charly = Banco_charly_new.objects.extra(select={'id_mensaje':'id_mensaje_c_n'}).filter(ingresado__year = anio ).order_by('ingresado')
                lista_notam_charly2 = Banco_charly_repla.objects.extra(select={'id_mensaje':'id_mensaje_c_r'}).filter(ingresado__month = mes ).order_by('ingresado')
                lista_notam_charly3 = Banco_charly_cancel.objects.extra(select={'id_mensaje':'id_mensaje_c_c'}).filter(ingresado__day = dia ).order_by('ingresado')
            else:
                lista_notam_charly = Banco_charly_new.objects.extra(select={'id_mensaje':'id_mensaje_c_n'}).filter(ingresado__range=[get_inicio, get_fin]).order_by('ingresado')
                    #lista_notam_charly = [ serializar_notam_banco_charly(notam) for notam in lista_notam_charly]
                lista_notam_charly2 = Banco_charly_repla.objects.extra(select={'id_mensaje':'id_mensaje_c_r'}).filter(ingresado__range=[get_inicio, get_fin]).order_by('ingresado')
                    #lista_notam_charly2 = [ serializar_notam_banco_charly(notam) for notam in lista_notam_charly2]
                lista_notam_charly3 = Banco_charly_cancel.objects.extra(select={'id_mensaje':'id_mensaje_c_c'}).filter(ingresado__range=[get_inicio, get_fin]).order_by('ingresado')
                    #lista_notam_charly3 = [ serializar_notam_banco_charly(notam) for notam in lista_notam_charly3]
            
            lista_notam_charly = sorted(chain(lista_notam_charly, lista_notam_charly2, lista_notam_charly3), key=attrgetter('ingresado'), reverse=True)
            lista_notam_charly = [ serializar_notam_banco_charly(notam) for notam in lista_notam_charly]


            return HttpResponse(json.dumps(lista_notam_charly), content_type='application/json')
        
        #-------------------------------------------------------------------------------------
        lista_notam_alfa=[]
        if 'alpha' in get_tipo:
            if get_inicio in get_fin:

                anio, mes, dia = get_inicio.split('-')

                lista_notam_alfa = Banco_alfa_new.objects.extra(select={'id_mensaje':'id_mensaje_a_n'}).filter(ingresado__year = anio ).order_by('ingresado')
                lista_notam_alfa2 = Banco_alfa_repla.objects.extra(select={'id_mensaje':'id_mensaje_a_r'}).filter(ingresado__month = mes ).order_by('ingresado')
                lista_notam_alfa3 = Banco_alfa_cancel.objects.extra(select={'id_mensaje':'id_mensaje_a_c'}).filter(ingresado__day = dia ).order_by('ingresado')

            else:
                lista_notam_alfa = Banco_alfa_new.objects.extra(select={'id_mensaje':'id_mensaje_a_n'}).filter(ingresado__range=[get_inicio, get_fin]).order_by('ingresado')
                    #lista_notam_alfa = [ serializar_notam_banco_alfa(notam) for notam in lista_notam_alfa]
                
                lista_notam_alfa2 = Banco_alfa_repla.objects.extra(select={'id_mensaje':'id_mensaje_a_r'}).filter(ingresado__range=[get_inicio, get_fin]).order_by('ingresado')
                    #lista_notam_alfa2 = [ serializar_notam_banco_alfa(notam) for notam in lista_notam_alfa2]
                
                lista_notam_alfa3 = Banco_alfa_cancel.objects.extra(select={'id_mensaje':'id_mensaje_a_c'}).filter(ingresado__range=[get_inicio, get_fin]).order_by('ingresado')
                    #lista_notam_alfa3 = [ serializar_notam_banco_alfa(notam) for notam in lista_notam_alfa3]

            lista_notam_alfa = sorted(chain(lista_notam_alfa, lista_notam_alfa2, lista_notam_alfa3), key=attrgetter('ingresado'), reverse=True)
            lista_notam_alfa = [ serializar_notam_banco_alfa(notam) for notam in lista_notam_alfa]


            #lista_notam_alfa += lista_notam_alfa2 + lista_notam_alfa3
            return HttpResponse(json.dumps(lista_notam_alfa), content_type='application/json')
        return HttpResponse(json.dumps([]), content_type='application/json')
    else:
        return redirect('login')
        


###########################################################################
##### BUSCADOR DE NOTAM
###########################################################################

def view_api_notam_search_string(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='TODOS_SERVICIOS').exists():
    # buscar notams
        get_parametro = str(request.GET.get('parametro'))
        get_tipo = str(request.GET.get('tipo'))

        dic={
            'lat' : '1658S',  
            'long' : '06508W',
            'radius'    : 5
        }
            
        if "codigoq" in get_tipo:
            sw=False
            lista_notam_amhs = []
            titulo="AMHS: CODIGO Q"
            if Amhs_charly_cancel.objects.filter(resumen__icontains=get_parametro).exists():
                lista_notam_amhs = Amhs_charly_cancel.objects.extra(select={'id_mensaje':'id_mensaje_c_c'}).filter(resumen__icontains=get_parametro).order_by('-ingresado')[:3]
                lista_notam_amhs = [ serializar_notam_banco_amhs_general(notam, titulo) for notam in lista_notam_amhs]
                sw = True

            if not sw and Amhs_charly_repla.objects.filter(resumen__icontains=get_parametro).exists():
                lista_notam_amhs = Amhs_charly_repla.objects.objects.extra(select={'id_mensaje':'id_mensaje_c_r'}).filter(resumen__icontains=get_parametro).order_by('-ingresado')[:3]
                lista_notam_amhs = [ serializar_notam_banco_amhs_general(notam, titulo) for notam in lista_notam_amhs]
                sw=True

            if not sw and Amhs_charly_new.objects.filter(resumen__icontains=get_parametro).exists():
                lista_notam_amhs = Amhs_charly_new.objects.extra(select={'id_mensaje':'id_mensaje_c_n'}).filter(resumen__icontains=get_parametro).order_by('-ingresado')[:3]
                lista_notam_amhs = [ serializar_notam_banco_amhs_general(notam, titulo) for notam in lista_notam_amhs]
                sw=True
            
            return render(request, 'temp_plan_vuelo/temp_aro_ais/modal_mensaje_query_string_after_search.html',{'notam_amhs':lista_notam_amhs, 'area':dic })
            #return HttpResponse(json.dumps(lista_notam_amhs), content_type='application/json')
            
        if "cuerpomsj" in get_tipo:
            sw=False
            lista_notam_amhs = []
            get_parametro = get_parametro.split('E) ')[0]
            titulo="AMHS: CUERPO DE MENSAJE E)"
            if Amhs_charly_cancel.objects.filter(mensaje__icontains=get_parametro).exists():
                lista_notam_amhs = Amhs_charly_cancel.objects.extra(select={'id_mensaje':'id_mensaje_c_c'}).filter(mensaje__icontains=get_parametro).order_by('-ingresado')[:3]
                lista_notam_amhs = [ serializar_notam_banco_amhs_general(notam, titulo) for notam in lista_notam_amhs]
                sw = True

            if not sw and Amhs_charly_repla.objects.filter(mensaje__icontains=get_parametro).exists():
                lista_notam_amhs = Amhs_charly_repla.objects.extra(select={'id_mensaje':'id_mensaje_c_r'}).filter(mensaje__icontains=get_parametro).order_by('-ingresado')[:3]
                lista_notam_amhs = [ serializar_notam_banco_amhs_general(notam, titulo) for notam in lista_notam_amhs]
                sw=True

            if not sw and Amhs_charly_new.objects.filter(mensaje__icontains=get_parametro).exists():
                lista_notam_amhs = Amhs_charly_new.objects.extra(select={'id_mensaje':'id_mensaje_c_n'}).filter(mensaje__icontains=get_parametro).order_by('-ingresado')[:3]
                lista_notam_amhs = [ serializar_notam_banco_amhs_general(notam, titulo) for notam in lista_notam_amhs]
                sw=True
            
            return render(request, 'temp_plan_vuelo/temp_aro_ais/modal_mensaje_query_string_after_search.html',{'notam_amhs':lista_notam_amhs, 'area':dic})
            #return HttpResponse(json.dumps(lista_notam_amhs), content_type='application/json')
            

        if "charlie" in get_tipo:
            sw=False
            notam_amhs=[{'titulo':'SIN RESULTADOS'}]
            titulo="AMHS: NOTAM CHARLIE"
            #### BUSCANDO EN EL TRAFICO AMHS
            if Amhs_charly_cancel.objects.filter(idnotam__startswith='('+get_parametro).exists():
                notam_amhs = Amhs_charly_cancel.objects.extra(select={'id_mensaje':'id_mensaje_c_c'}).filter(idnotam__startswith='('+get_parametro)[0]
                notam_amhs = serializar_notam_banco_amhs_general(notam_amhs, titulo)
                notam_amhs = [notam_amhs]
                sw = True
            if Amhs_charly_cancel.objects.filter(idnotam__startswith='('+get_parametro).exists():
                notam_amhs = Amhs_charly_cancel.objects.extra(select={'id_mensaje':'id_mensaje_c_c'}).filter(idnotam__startswith='('+get_parametro)[0]
                notam_amhs = serializar_notam_banco_amhs_general(notam_amhs, titulo)
                notam_amhs = [notam_amhs]
                sw = True


            if not sw and Amhs_charly_repla.objects.filter(idnotam__startswith='('+get_parametro).exists():
                notam_amhs = Amhs_charly_repla.objects.extra(select={'id_mensaje':'id_mensaje_c_r'}).filter(idnotam__startswith='('+get_parametro)[0]
                notam_amhs = serializar_notam_banco_amhs_general(notam_amhs, titulo)
                notam_amhs = [notam_amhs]
                sw=True

            if not sw and Amhs_charly_new.objects.filter(idnotam__startswith='('+get_parametro).exists():
                notam_amhs = Amhs_charly_new.objects.extra(select={'id_mensaje':'id_mensaje_c_n'}).filter(idnotam__startswith='('+get_parametro)[0]
                notam_amhs = serializar_notam_banco_amhs_general(notam_amhs, titulo)
                notam_amhs = [notam_amhs]
                sw=True


            #### BUSCANDO EN EL BANCO NOF
            sw_banco_nof=False
            if Banco_charly_new.objects.filter(id_mensaje_c_n=get_parametro).exists():
                sw_banco_nof=True
                notam_banco = Banco_charly_new.objects.extra(select={'id_mensaje':'id_mensaje_c_n'}).get(id_mensaje_c_n=get_parametro)
            if Banco_charly_repla.objects.filter(id_mensaje_c_r=get_parametro).exists():
                sw_banco_nof=True
                notam_banco = Banco_charly_repla.objects.extra(select={'id_mensaje':'id_mensaje_c_r'}).get(id_mensaje_c_r=get_parametro)
            if Banco_charly_cancel.objects.filter(id_mensaje_c_c=get_parametro).exists():
                sw_banco_nof=True
                notam_banco = Banco_charly_cancel.objects.extra(select={'id_mensaje':'id_mensaje_c_c'}).get(id_mensaje_c_c=get_parametro)
            
            if sw_banco_nof:
                notam_banco = serializar_notam_banco_charly(notam_banco)
            else:
                notam_banco = []
            return render(request, 'temp_plan_vuelo/temp_aro_ais/modal_mensaje_query_string_after_search.html',{'notam_amhs':notam_amhs, 'notam_banco':notam_banco, 'area':dic})
            #return HttpResponse(json.dumps(notam_amhs), content_type='application/json')

        if "alpha" in get_tipo:
            sw=False
            notam_amhs=[{'titulo':'SIN RESULTADOS'}]
            titulo="AMHS: NOTAM ALPHA"
            if Amhs_alfa_cancel.objects.filter(idnotam__icontains=get_parametro).exists():
                notam_amhs = Amhs_alfa_cancel.objects.extra(select={'id_mensaje':'id_mensaje_a_c'}).filter(idnotam__icontains=get_parametro)[0]
                notam_amhs = serializar_notam_banco_amhs_general(notam_amhs, titulo)
                notam_amhs = [notam_amhs]
                sw = True

            if not sw and Amhs_alfa_repla.objects.filter(idnotam__icontains=get_parametro).exists():
                notam_amhs = Amhs_alfa_repla.objects.extra(select={'id_mensaje':'id_mensaje_a_r'}).filter(idnotam__icontains=get_parametro)[0]
                notam_amhs = serializar_notam_banco_amhs_general(notam_amhs, titulo)
                notam_amhs = [notam_amhs]
                sw=True

            if not sw and Amhs_alfa_new.objects.filter(idnotam__icontains=get_parametro).exists():
                notam_amhs = Amhs_alfa_new.objects.extra(select={'id_mensaje':'id_mensaje_a_n'}).filter(idnotam__icontains=get_parametro)[0]
                notam_amhs = serializar_notam_banco_amhs_general(notam_amhs, titulo)
                notam_amhs = [notam_amhs]
                sw=True
            
            #### BUSCANDO EN EL BANCO NOF
            sw_banco_nof=False
            if Banco_alfa_new.objects.filter(id_mensaje_a_n=get_parametro).exists():
                sw_banco_nof=True
                notam_banco = Banco_alfa_new.objects.extra(select={'id_mensaje':'id_mensaje_a_n'}).get(id_mensaje_a_n=get_parametro)
            if Banco_alfa_repla.objects.filter(id_mensaje_a_r=get_parametro).exists():
                sw_banco_nof=True
                notam_banco = Banco_alfa_repla.objects.extra(select={'id_mensaje':'id_mensaje_a_r'}).get(id_mensaje_a_r=get_parametro)
            if Banco_alfa_cancel.objects.filter(id_mensaje_a_c=get_parametro).exists():
                sw_banco_nof=True
                notam_banco = Banco_alfa_cancel.objects.extra(select={'id_mensaje':'id_mensaje_a_c'}).get(id_mensaje_a_c=get_parametro)
            
            if sw_banco_nof:
                notam_banco = serializar_notam_banco_charly(notam_banco)
            else:
                notam_banco = []

            return render(request, 'temp_plan_vuelo/temp_aro_ais/modal_mensaje_query_string_after_search.html',{'notam_amhs':notam_amhs, 'notam_banco':notam_banco, 'area':dic})
            #return HttpResponse(json.dumps(notam_amhs), content_type='application/json')
    
        return render(request, 'temp_plan_vuelo/temp_aro_ais/modal_mensaje_query_string_after_search.html',{'notam_amhs':[], 'area':dic})
        #return HttpResponse(json.dumps([]), content_type='application/json')
    else:
        return redirect('login')

def serializar_notam_banco_amhs_general(notam, titulo):
    if 'D) ' in notam.mensaje:
        casilla_d , casilla_e = notam.mensaje.split('E) ')
        casilla_e = 'E) '+ casilla_e
    else:
        casilla_d=""
        casilla_e=notam.mensaje
    return {
        'titulo':titulo,
        'aftn1': notam.aftn2,
        'id_mensaje': notam.id_mensaje,
        'aftn1': notam.aftn1,
        'aftn2': notam.aftn2,
        'idnotam': notam.idnotam,
        'resumen': notam.resumen,
        'aplica_a': notam.aplica_a,
        'valido_desde': notam.valido_desde,
        'valido_hasta': notam.valido_hasta,
        'mensaje': notam.mensaje,
        'casilla_d': casilla_d,
        'casilla_e': casilla_e,
    }



###########################################################################
##### APP VERSIONADO DEL PIB
###########################################################################

def serializar_pibtrafico_pibextenso(pibloong):
    if str(pibloong.decodificado).strip().index("E)") >0:
        decodificado=str(pibloong.decodificado).strip()[ str(pibloong.decodificado).strip().index("E)")+2 :-1 ] 
    else:
        decodificado=""
    return {
        'ref_notam_amhs_id' : str(pibloong.ref_notam_amhs_id).strip().upper(),
        'decodificado' : decodificado.upper(),
        'publicado' : str(pibloong.publicado).strip().upper(),
        'vigente' : str(pibloong.vigente).strip().upper(),
        'archivado' : str(pibloong.archivado).strip().upper(),
        'oficialaro_id' : str(pibloong.oficialaro_id).strip().upper(),
        'pendiente' : str(pibloong.pendiente).strip().upper(),
        'msj_publicado' : str(pibloong.msj_publicado).strip().upper(),
        'instalacion' : str(pibloong.instalacion).strip().upper(),
        'notam_extenso_id' : str(pibloong.notam_extenso_id).strip().upper(),
        'notam_id' : str(pibloong.notam_id).strip().upper(),
        'notam_tipo' : str(pibloong.notam_tipo).strip().upper(),
        'ref_notam_id' : str(pibloong.ref_notam_id).strip().upper(),
        'fir' : str(pibloong.fir).strip().upper(),
        'notam_codigo' : str(pibloong.notam_codigo).strip().upper(),
        'tipo_trafico' : str(pibloong.tipo_trafico).strip().upper(),
        'proposito' : str(pibloong.proposito).strip().upper(),
        'alcance' : str(pibloong.alcance).strip().upper(),
        'fl_inferior' : str(pibloong.fl_inferior).strip().upper(),
        'fl_superior' : str(pibloong.fl_superior).strip().upper(),
        'area' : str(pibloong.area).strip().upper(),
        'lugar' : str(pibloong.lugar).strip().upper(),
        'valid_desde' : str(pibloong.valid_desde).strip().upper(),
        'valid_hasta' : str(pibloong.valid_hasta).strip().upper(),
        'agendado' : str(pibloong.agendado).strip().upper(),
        'cuerpo' : str(pibloong.cuerpo).strip().upper(),
        'limit_superior' : str(pibloong.limit_superior).strip().upper(),
        'limit_inferior' : str(pibloong.limit_inferior).strip().upper(),
        'indices_item_a' : str(pibloong.indices_item_a).strip().upper(),
        'indices_item_b' : str(pibloong.indices_item_b).strip().upper(),
        'indices_item_c' : str(pibloong.indices_item_c).strip().upper(),
        'indices_item_d' : str(pibloong.indices_item_d).strip().upper(),
        'indices_item_e' : str(pibloong.indices_item_e).strip().upper(),
        'indices_item_f' : str(pibloong.indices_item_f).strip().upper(),
        'indices_item_g' :str(pibloong.indices_item_g).strip().upper(),
    }

def view_archivar_pib(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AROAISLP').exists():
        if request.is_ajax and request.method =="GET":
            getid_mensaje = request.GET.dict()['id_notam']
            gettipo = request.GET.dict()['tipo']
            
            pib_Trafico=Pib_trafico.objects.filter(ref_notam_amhs_id=getid_mensaje)
            
            if pib_Trafico.exists():
                if gettipo in 'archivar':
                    Pib_trafico.objects.filter(ref_notam_amhs_id=getid_mensaje).update(archivado=True, pendiente=False, vigente=False)
                else:
                    Pib_trafico.objects.filter(ref_notam_amhs_id=getid_mensaje).update(archivado=False, pendiente=True, vigente=False)
                
                return JsonResponse({'estado':True}, status=200)

        return JsonResponse({'estado':False}, status=200)
    else:
        return redirect('accounts/login/')

def view_publicarguardar_pib(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AROAISLP').exists():
        if request.is_ajax and request.method =="GET":
            getid_mensaje = request.GET.dict()['id_notam']
            
            pib_Trafico=Pib_trafico.objects.filter(ref_notam_amhs_id=getid_mensaje)
            if pib_Trafico.exists():
                getpublicacion = request.GET.dict()['publicacion']
                gettrabajador = request.GET.dict()['persona']
                getinstalacion = request.GET.dict()['instalacion']
                Pib_trafico.objects.filter(ref_notam_amhs_id=getid_mensaje).update(oficialaro_id=gettrabajador, msj_publicado=getpublicacion, instalacion=getinstalacion, pendiente=False, archivado=False, vigente=True, publicado=datetime.datetime.now())
                return JsonResponse({'estado':True}, status=200)

        return JsonResponse({'estado':False}, status=200)
    else:
        return redirect('accounts/login/')


def view_guardarregistro_pib(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AROAISLP').exists():
        if request.is_ajax and request.method =="GET":
            getresumen = request.GET.dict()['resumen']

            getresumen=getresumen.split(',')

            sw=True
            #verificando que todos los notams existan
            for pib in getresumen:
                if pib != "":
                    if not Pib_trafico.objects.filter(ref_notam_amhs_id=pib).exists():
                        sw=False
            if sw:
                gettrabajador = request.GET.dict()['oficial']
                
                documento = Pib_registro_documento()


                documento.oficialaro=Trabajador.objects.get(ci=gettrabajador)
                documento.save()
                
                for pib in getresumen:
                    if pib != "":
                        documento.registro.add(pib)
                
                
                return JsonResponse({'estado':True}, status=200)
        return JsonResponse({'estado':False}, status=200)
    else:
        return redirect('accounts/login/')

    


def view_pib_tiemporeal(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='TODOS_SERVICIOS').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")

        equipo_activo = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and activo=true and empresa_institucion_id=1 order by activo")
        
        return render(request, 'temp_plan_vuelo/temp_aro_ais/notam_realtime.html' ,{'equipo_activo':equipo_activo,'equipo_trabajo': equipo_coordinacion, } )
    else:
        return redirect('login')
    
def view_pib_tiemporeal2(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='TODOS_SERVICIOS').exists():
        return render(request, 'temp_plan_vuelo/temp_aro_ais/notam_realtime2.html' )
    else:
        return redirect('login')



def view_pibupdate_tiemporeal(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='TODOS_SERVICIOS').exists():
        if request.is_ajax and request.method =="GET":
            #obteniendo aeropuertos
            lista_aeropuerto =  Aeropuerto.objects.all().only('icao').order_by('icao')

            #Pib_trafico.objects.raw("select ref_notam_amhs_id, decodificado, publicado, vigente, oficialaro_id, msj_publicado, notam_id, notam_tipo, ref_notam_id, fir, notam_codigo, tipo_trafico, proposito, alcance, fl_inferior, fl_superior, area, lugar, valid_desde, valid_hasta, agendado, cuerpo, limit_superior, limit_inferior from aro_ais_pib_trafico inner join aro_ais_pib_extenso on ref_notam_amhs_id = notam_extenso_id and vigente='t' and msj_publicado!='' and  DATE(publicado)>='2020-09-21' and lugar like %(icao)s  ", {'icao':'%'+aeroicao+'%'})
            # ref_notam_amhs_id | decodificado | publicado | vigente |  oficialaro_id |  msj_publicado |     
            # notam_id | notam_tipo | ref_notam_id | fir  | notam_codigo |  tipo_trafico  | proposito |    alcance    | fl_inferior | fl_superior | 
            # area |  lugar   |      valid_desde       |      valid_hasta       |   agendado    | cuerpo | limit_superior | limit_inferior | 
            ###estoy buscando los pibs recientes , vigentes, y publicados
            lista_pib_por_region = [ {'icao':aero.icao, 'pibs':  [ serializarPibRegional(pibregional) for pibregional in Pib_trafico.objects.raw("select ref_notam_amhs_id, decodificado, publicado, instalacion, vigente, oficialaro_id, msj_publicado, notam_id, notam_tipo, ref_notam_id, fir, notam_codigo, tipo_trafico, proposito, alcance, fl_inferior, fl_superior, area, lugar, valid_desde, valid_hasta, agendado, cuerpo, limit_superior, limit_inferior from aro_ais_pib_trafico inner join aro_ais_pib_extenso on ref_notam_amhs_id = notam_extenso_id and vigente='t' and msj_publicado!='' and  DATE(publicado)>='2020-09-21' and lugar like %(icao)s  ", {'icao':'%'+aero.icao+'%'}) ],  } for aero in lista_aeropuerto]

            '''          
                ref_notam_amhs_id
                decodificado
                publicado
                vigente
                oficialaro_id
                msj_publicado
                notam_id
                notam_tipo
                ref_notam_id
                fir
                notam_codigo
                tipo_trafico
                proposito
                alcance
                fl_inferior
                fl_superior
                area
                lugar
                valid_desde
                valid_hasta
                agendado
                cuerpo
                limit_superior
                limit_inferior
            '''
            return HttpResponse(json.dumps(lista_pib_por_region), status=200)

        return JsonResponse({'estado':False}, status=200)
    else:
        return redirect('accounts/login/')


def serializarPibRegional(pibicao):
    return { 
        'ref_notam_amhs_id' : str(pibicao.ref_notam_amhs_id).upper(), 
        'decodificado' : str(pibicao.decodificado).upper(), 
        'publicado' : str(pibicao.publicado).upper(), 
        'vigente' : str(pibicao.vigente).upper(), 
        'oficialaro_id' : str(pibicao.oficialaro_id).upper(), 
        'msj_publicado' : str(pibicao.msj_publicado).upper(), 
        'instalacion' : str(pibicao.instalacion).upper(), 
        'notam_id' : str(pibicao.notam_id).upper(), 
        'notam_tipo' : str(pibicao.notam_tipo).upper(), 
        'ref_notam_id' : str(pibicao.ref_notam_id).upper(), 
        'fir' : str(pibicao.fir).upper(), 
        'notam_codigo' : str(pibicao.notam_codigo).upper(), 
        'tipo_trafico' : str(pibicao.tipo_trafico).upper(), 
        'proposito' : str(pibicao.proposito).upper(), 
        'alcance' : str(pibicao.alcance).upper(), 
        'fl_inferior' : str(pibicao.fl_inferior).upper(), 
        'fl_superior' : str(pibicao.fl_superior).upper(), 
        'area' : str(pibicao.area).upper(), 
        'lugar' : str(pibicao.lugar).upper(), 
        'valid_desde' : str(pibicao.valid_desde).upper(), 
        'valid_hasta' : str(pibicao.valid_hasta).upper(), 
        'agendado' : str(pibicao.agendado).upper(), 
        'cuerpo' : str(pibicao.cuerpo).upper(), 
        'limit_superior' : str(pibicao.limit_superior).upper(), 
        'limit_inferior' : str(pibicao.limit_inferior).upper(),
    }





# AIM ################################################################################################################

def view_get_abreviatura8400(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
        #equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        if request.method =="GET":
            #get_abreviatura = str(request.GET.dict()['abreviatura'])
            get_abreviatura = str(request.GET.get('abreviatura'))
            #buscamos coincidencias en SIGNIFICADO_COMPLETO o ABREVIATURA
            #id_significado | abreviatura | significado_completo |         significado_pib
            lista_abreviaturas = Abreviatura_8400.objects.raw("select id_significado, abreviatura,significado_completo, significado_pib from aro_ais_abreviatura_8400 inner join aro_ais_significado_8400 on abreviatura_id=abreviatura where abreviatura like %(abreviatura)s" , { 'abreviatura' : str("%"+get_abreviatura+"%")} )
            lista_textoclaro = Abreviatura_8400.objects.raw("select id_significado, abreviatura,significado_completo, significado_pib from aro_ais_abreviatura_8400 inner join aro_ais_significado_8400 on abreviatura_id=abreviatura where significado_completo like %(abreviatura2)s" , { 'abreviatura2' : "%"+get_abreviatura+"%"} )

            lista_abreviaturas = [ serializarAbreviatura(abrev) for abrev in lista_abreviaturas ]
            lista_textoclaro = [ serializarAbreviatura(abrev) for abrev in lista_textoclaro ]
            #
            devolucion = {
                'abreviaturas': lista_abreviaturas,
                'texto_claro': lista_textoclaro
            }

            return HttpResponse(json.dumps(devolucion), content_type='application/json')
        else:
            return HttpResponse(json.dumps([{'HOLA':'hola'}]), content_type='application/json')
    else:
        return redirect('login')


def serializarAbreviatura(abrev):
    return {
        'id_significado' : abrev.id_significado,
        'abreviatura' : abrev.abreviatura,
        'significado_completo' : abrev.significado_completo,
        'significado_pib' : abrev.significado_pib,
    }


def view_get_codigo8126(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
        #equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        if request.method =="GET":
            #get_abreviatura = str(request.GET.dict()['abreviatura'])
            get_codigo_asunto = str(request.GET.get('string8126')).upper()
            #buscamos coincidencias en SIGNIFICADO_COMPLETO o ABREVIATURA
            
            #id_significado | abreviatura | significado_completo |         significado_pib
            titulo_letra = Letra_asunto.objects.raw("select id_letra, titulo_letra, acronimo from aro_ais_letra_asunto where id_letra in ( select letra_asunto_id from aro_ais_asunto where id_asunto like %(codigo_asunto)s  ) " , { 'codigo_asunto' : str("%"+get_codigo_asunto+"%")} )
            if len(titulo_letra) > 0:
                acronimo_letra = str(titulo_letra[0].acronimo + " - ")
                titulo_letra = str(titulo_letra[0].titulo_letra)
            else:
                titulo_letra=""
                acronimo_letra=""


            #id_asunto | descripcion_asunto | fraseologia_asunto
            lista_asuntos = Asunto.objects.raw("select id_asunto, descripcion_asunto, fraseologia_asunto from aro_ais_asunto where id_asunto like %(codigo_asunto)s" , { 'codigo_asunto' : ""+get_codigo_asunto+""} )
            lista_asuntos = [ serializarAsunto(codig) for codig in lista_asuntos ]

            ## BUSCQUEDA A PARTIR DE UN ASUNTO
            #id_estado_asunto | descripcion_estado | fraseologia_estado
            lista_estados = []
            lista_estados = Estado_asunto.objects.raw("SELECT * from aro_ais_estado_asunto where id_estado_asunto in (select estado_asunto_id from aro_ais_estado_asunto_id_asunto where asunto_id like %(codigo_asunto)s) " , { 'codigo_asunto' : ""+get_codigo_asunto+""} )
            lista_estados = [ serializarEstadoAsunto(estado) for estado in lista_estados ]
            
            ## BUSQUEDA A PARTIR DEL ESTADO_ASUNTO
            #id_estado_asunto | descripcion_estado | fraseologia_estado
            lista_estados2 = Estado_asunto.objects.raw("select * from aro_ais_estado_asunto where id_estado_asunto like %(codigo_asunto)s " , { 'codigo_asunto' : ""+get_codigo_asunto+""} )
            lista_estados2 = [ serializarEstadoAsunto(estado) for estado in lista_estados2 ]
            

            lista_estados.extend(lista_estados2)
            #
            devolucion = {
                'titulo_letra' : titulo_letra,
                'acronimo_letra': acronimo_letra,
                'asuntos': lista_asuntos,
                'estados_asuntos': lista_estados,
            }

            return HttpResponse(json.dumps(devolucion), content_type='application/json')
        else:
            return HttpResponse(json.dumps([{'HOLA':'hola'}]), content_type='application/json')
    else:
        return redirect('login')

def serializarAsunto(cod):
    return {
        'id_asunto' : cod.id_asunto,
        'descripcion_asunto' : cod.descripcion_asunto,
        'fraseologia_asunto' : cod.fraseologia_asunto,
    }
def serializarEstadoAsunto(estado):
    return {
        'id_estado_asunto' : estado.id_estado_asunto,
        'descripcion_estado' : estado.descripcion_estado,
        'fraseologia_estado' : estado.fraseologia_estado,
    }



def view_get_lista_asuntos_8126(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
        #equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        if request.method =="GET":
            #get_abreviatura = str(request.GET.dict()['abreviatura'])
            get_letra = str(request.GET.get('string8126')).upper()
            #buscamos coincidencias en SIGNIFICADO_COMPLETO o ABREVIATURA
            
            # id_asunto | descripcion_asunto | fraseologia_asunto
            lista_asuntos = Asunto.objects.raw("select * from aro_ais_asunto where letra_asunto_id like  %(letra)s order by id_asunto asc" , { 'letra' : ""+get_letra+""} )

            lista_asuntos = [ serializarLista_Asuntos(codig) for codig in lista_asuntos ]

            devolucion = {
                'lista_asuntos': lista_asuntos,
            }

            return HttpResponse(json.dumps(devolucion), content_type='application/json')
        else:
            return HttpResponse(json.dumps([{'HOLA':'hola'}]), content_type='application/json')
    else:
        return redirect('login')

def serializarLista_Asuntos(asunto):
    return {
        'id_asunto' : asunto.id_asunto,
        'descripcion_asunto' : asunto.descripcion_asunto,
        'fraseologia_asunto' : asunto.fraseologia_asunto,
    }



def view_get_lista_estados_8126(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
        #equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        if request.method =="GET":
            #get_abreviatura = str(request.GET.dict()['abreviatura'])
            get_asunto = str(request.GET.get('string8126')).upper()
            #buscamos coincidencias en SIGNIFICADO_COMPLETO o ABREVIATURA
            
            # id_estado_asunto | descripcion_estado | fraseologia_estado
            lista_estados = Estado_asunto.objects.raw("select id_estado_asunto, descripcion_estado, fraseologia_estado from  aro_ais_estado_asunto as tx2 inner join  aro_ais_estado_asunto_id_asunto as tx1 on tx2.id_estado_asunto like tx1.estado_asunto_id where tx1.asunto_id like %(asunto)s order by id_estado_asunto asc" , { 'asunto' : ""+get_asunto+""} )

            lista_estados = [ serializarLista_Estados(estado) for estado in lista_estados ]

            devolucion = {
                'lista_estados': lista_estados,
            }

            return HttpResponse(json.dumps(devolucion), content_type='application/json')
        else:
            return HttpResponse(json.dumps([{'HOLA':'hola'}]), content_type='application/json')
    else:
        return redirect('login')

def serializarLista_Estados(estado):
    return {
        'id_estado_asunto' : estado.id_estado_asunto,
        'descripcion_estado' : estado.descripcion_estado,
        'fraseologia_estado' : estado.fraseologia_estado,
    }

##CREAR NOTAM
from appUpsilon.views import view_pagina_principal  # , control_acceso_login
def view_post_crear_notam(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
        if request.method =="POST" and request.POST:
            post_tipo = str(request.POST.get('tipo'))
            var_file = request.FILES['formulario_oaci']
            notam_destino = str(request.POST.get('notam_destino'))
            
            inf_constante = {
                'post_amhs1' : str(request.POST.get('amhs1')),
                'post_amhs2' : str(request.POST.get('amhs2')),
                'post_resumen' : str(request.POST.get('resumen')),
                'post_aplica_a' : str(request.POST.get('aplica_a')),
                'post_valido_desde' : str(request.POST.get('valido_desde')),
                'post_valido_hasta' : str(request.POST.get('valido_hasta')),
                #'post_mensaje' : str(request.POST.get('mensaje')),

                'post_mensaje_charly' : str(request.POST.get('mensaje_charly')),
                'post_mensaje_alfa' : str(request.POST.get('mensaje_alfa')),

                'post_asunto' : str(request.POST.get('asunto')),
                'post_estado_asunto' : str(request.POST.get('estado_asunto')),
                'post_estimado' : str(request.POST.get('estimado')),
                'post_permanente' : str(request.POST.get('permanente')),
                'antecedente' : str(request.POST.get('antecedente')),
                'responsable' : str(request.POST.get('responsable')),
            }

            if notam_destino:
                charly_destino, alfa_destino = notam_destino.split('+')
            else:
                charly_destino, alfa_destino = '',''

            ############ CONTROL DE ID_MENSAJE           
            id_charly=""
            id_alfa=""

            post_notam_header = str(request.POST.get('notam_header'))
            array_notam_header = post_notam_header.split("+")
            for id_n in array_notam_header:
                if id_n:
                    if 'C' in id_n:
                        id_charly=id_n
                    if 'A' in id_n:
                        id_alfa=id_n
            ############ CONTROL DE ID_MENSAJE       
            
            post_pib_publicar = str(request.POST.get('pib_publicar'))



            ########### CONTROL DE ID_NOTAM           
            if id_charly:
                if 'NOTAMN' in post_tipo:
                    guardar_nuevo_charly(id_charly, inf_constante, post_pib_publicar, var_file, id_alfa)
                if 'NOTAMR' in post_tipo:
                    guardar_repla_charly(id_charly, charly_destino, inf_constante, post_pib_publicar, var_file, id_alfa)
                if 'NOTAMC' in post_tipo:
                    guardar_cancel_charly(id_charly, charly_destino, inf_constante, var_file, id_alfa)
            if id_alfa:
                if 'NOTAMN' in post_tipo:
                    guardar_nuevo_alfa(id_alfa, inf_constante, var_file, id_charly)
                if 'NOTAMR' in post_tipo:
                    guardar_repla_alfa(id_alfa, alfa_destino, inf_constante, var_file, id_charly)
                if 'NOTAMC' in post_tipo:
                    guardar_cancel_alfa(id_alfa, alfa_destino, inf_constante, var_file, id_charly)
            
            ############ CONTROL DE ID_NOTAM           

            #return render(request, 'temp_ais_nacional/blanco.html',{'devolucion':devolucion})
            return HttpResponseRedirect(reverse( view_pagina_principal ))
        else:
            return redirect('view_new_notam' )
            #return render(request, 'temp_plan_vuelo/temp_aro_ais/new_notam.html' , locals())
            #return HttpResponse(json.dumps([{'Response':'Envie datos validos.'}]), content_type='application/json')
    else:
        return redirect('login')


## FUNCIONES PARA GUARDAR NOTAM CLASIFICADO
def guardar_nuevo_charly(id_charly, inf_constante, post_pib_publicar, var_file, correlativo_alfa):
    banco_charly=Banco_charly_new()

    banco_charly.id_mensaje_c_n = id_charly
    banco_charly.aftn1 = inf_constante['post_amhs1']
    banco_charly.aftn2 = inf_constante['post_amhs2']
    banco_charly.idnotam = '(' +id_charly + ' NOTAMN'
    banco_charly.resumen = inf_constante['post_resumen']
    banco_charly.aplica_a = inf_constante['post_aplica_a']
    banco_charly.valido_desde = inf_constante['post_valido_desde']
    banco_charly.valido_hasta = inf_constante['post_valido_hasta']
    banco_charly.mensaje = inf_constante['post_mensaje_charly']

    if 'EST' in inf_constante['post_estimado']:
        banco_charly.est = True
    if 'PERM' in inf_constante['post_permanente']:
        banco_charly.perm = True

    banco_charly.es_pib = True

    banco_charly.asunto = inf_constante['post_asunto']
    banco_charly.estado_asunto = inf_constante['post_estado_asunto']

    banco_charly.pib_publicar = post_pib_publicar
    
    banco_charly.antecedente = inf_constante['antecedente']

    banco_charly.responsable = inf_constante['responsable']
    banco_charly.correlativo_alfa = correlativo_alfa
    
    banco_charly.form_oaci = var_file 

    banco_charly.save()

def guardar_repla_charly(id_charly, notam_destino, inf_constante, post_pib_publicar, var_file, correlativo_alfa):
    banco_charly=Banco_charly_repla()

    banco_charly.id_mensaje_c_r = id_charly
    banco_charly.aftn1 = inf_constante['post_amhs1']
    banco_charly.aftn2 = inf_constante['post_amhs2']
    banco_charly.idnotam = '(' +id_charly + ' NOTAMR ' + notam_destino
    banco_charly.resumen = inf_constante['post_resumen']
    banco_charly.aplica_a = inf_constante['post_aplica_a']
    banco_charly.valido_desde = inf_constante['post_valido_desde']
    banco_charly.valido_hasta = inf_constante['post_valido_hasta']
    banco_charly.mensaje = inf_constante['post_mensaje_charly']

    if 'EST' in inf_constante['post_estimado']:
        banco_charly.est = True
    if 'PERM' in inf_constante['post_permanente']:
        banco_charly.perm = True

    banco_charly.es_pib = True

    banco_charly.asunto = inf_constante['post_asunto']
    banco_charly.estado_asunto = inf_constante['post_estado_asunto']

    banco_charly.pib_publicar = post_pib_publicar
    
    banco_charly.antecedente = inf_constante['antecedente']

    banco_charly.responsable = inf_constante['responsable']
    banco_charly.correlativo_alfa = correlativo_alfa
    
    banco_charly.form_oaci = var_file #inf_constante['formulario_oaci']

    banco_charly.save()

def guardar_cancel_charly(id_charly, notam_destino, inf_constante, var_file, correlativo_alfa):
    banco_charly=Banco_charly_cancel()

    banco_charly.id_mensaje_c_c = id_charly
    banco_charly.aftn1 = inf_constante['post_amhs1']
    banco_charly.aftn2 = inf_constante['post_amhs2']
    banco_charly.idnotam = '(' +id_charly + ' NOTAMC ' + notam_destino
    banco_charly.resumen = inf_constante['post_resumen']
    banco_charly.aplica_a = inf_constante['post_aplica_a']
    banco_charly.valido_desde = inf_constante['post_valido_desde']
    banco_charly.valido_hasta = inf_constante['post_valido_hasta']
    banco_charly.mensaje = inf_constante['post_mensaje_charly']

    banco_charly.asunto = inf_constante['post_asunto']
    banco_charly.estado_asunto = inf_constante['post_estado_asunto']

    banco_charly.antecedente = inf_constante['antecedente']

    banco_charly.responsable = inf_constante['responsable']
    banco_charly.correlativo_alfa = correlativo_alfa
        
    banco_charly.form_oaci = var_file #inf_constante['formulario_oaci']

    banco_charly.save()

#######################################
#######
def guardar_nuevo_alfa(id_alfa, inf_constante, var_file, correlativo_charly):
    banco_alfa=Banco_alfa_new()

    banco_alfa.id_mensaje_a_n = id_alfa
    banco_alfa.aftn1 = inf_constante['post_amhs1']
    banco_alfa.aftn2 = inf_constante['post_amhs2']
    banco_alfa.idnotam = '('+id_alfa + ' NOTAMN'
    banco_alfa.resumen = inf_constante['post_resumen']
    banco_alfa.aplica_a = inf_constante['post_aplica_a']
    banco_alfa.valido_desde = inf_constante['post_valido_desde']
    banco_alfa.valido_hasta = inf_constante['post_valido_hasta']
    banco_alfa.mensaje = inf_constante['post_mensaje_alfa']

    if inf_constante['post_estimado']:
        banco_alfa.est = True
    if inf_constante['post_permanente']:
        banco_alfa.perm = True

    banco_alfa.asunto = inf_constante['post_asunto']
    banco_alfa.estado_asunto = inf_constante['post_estado_asunto']

    banco_alfa.antecedente = inf_constante['antecedente']
    
    banco_alfa.responsable = inf_constante['responsable']
    banco_alfa.correlativo_charly = correlativo_charly

    banco_alfa.form_oaci = var_file 
    banco_alfa.save()

def guardar_repla_alfa(id_alfa, notam_destino, inf_constante, var_file, correlativo_charly):
    banco_alfa=Banco_alfa_repla()

    banco_alfa.id_mensaje_a_r = id_alfa
    banco_alfa.aftn1 = inf_constante['post_amhs1']
    banco_alfa.aftn2 = inf_constante['post_amhs2']
    banco_alfa.idnotam = '('+id_alfa + ' NOTAMR ' + notam_destino
    banco_alfa.resumen = inf_constante['post_resumen']
    banco_alfa.aplica_a = inf_constante['post_aplica_a']
    banco_alfa.valido_desde = inf_constante['post_valido_desde']
    banco_alfa.valido_hasta = inf_constante['post_valido_hasta']
    banco_alfa.mensaje = inf_constante['post_mensaje_alfa']

    if inf_constante['post_estimado']:
        banco_alfa.est = True
    if inf_constante['post_permanente']:
        banco_alfa.perm = True

    banco_alfa.asunto = inf_constante['post_asunto']
    banco_alfa.estado_asunto = inf_constante['post_estado_asunto']

    banco_alfa.antecedente = inf_constante['antecedente']
    
    banco_alfa.responsable = inf_constante['responsable']
    banco_alfa.correlativo_charly = correlativo_charly

    banco_alfa.form_oaci = var_file #inf_constante['formulario_oaci']

    banco_alfa.save()

def guardar_cancel_alfa(id_alfa, notam_destino, inf_constante, var_file, correlativo_charly):
    banco_alfa=Banco_alfa_cancel()

    banco_alfa.id_mensaje_a_c = id_alfa
    banco_alfa.aftn1 = inf_constante['post_amhs1']
    banco_alfa.aftn2 = inf_constante['post_amhs2']
    banco_alfa.idnotam = '('+id_alfa + ' NOTAMC ' + notam_destino
    banco_alfa.resumen = inf_constante['post_resumen']
    banco_alfa.aplica_a = inf_constante['post_aplica_a']
    banco_alfa.valido_desde = inf_constante['post_valido_desde']
    banco_alfa.valido_hasta = inf_constante['post_valido_hasta']
    banco_alfa.mensaje = inf_constante['post_mensaje_alfa']

    banco_alfa.asunto = inf_constante['post_asunto']
    banco_alfa.estado_asunto = inf_constante['post_estado_asunto']

    banco_alfa.antecedente = inf_constante['antecedente']

    banco_alfa.responsable = inf_constante['responsable']
    banco_alfa.correlativo_charly = correlativo_charly

    banco_alfa.form_oaci = var_file #inf_constante['formulario_oaci']

    banco_alfa.save()



def view_get_correlativo_charly(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
        if request.method =="GET":
            get_anio = str(datetime.datetime.now().year)[2:]
            lista_correlativos = Banco_charly_repla.objects.raw("select * from ( 	select id_mensaje_c_r,substring( id_mensaje_c_r, 2, 4) as idnotam 	from aro_ais_notam_trafico_charly_repla 	where id_mensaje_c_r like %(anio)s 	union  	select id_mensaje_c_n,substring( id_mensaje_c_n, 2, 4) as idnotam 	from aro_ais_notam_trafico_charly_new 	where id_mensaje_c_n like %(anio)s 	union  	select id_mensaje_c_c,substring( id_mensaje_c_c, 2, 4)  as idnotam 	from aro_ais_notam_trafico_charly_cancel 	where id_mensaje_c_c like %(anio)s ) as t_correlativo order by  idnotam desc limit 1" , { 'anio' : "%/"+get_anio} )
            if len(lista_correlativos) > 0:
                correlativo = "C" + str(int(lista_correlativos[0].idnotam)+1) + "/" + get_anio
            else:
                correlativo = 'C0001/' + get_anio

            devolucion = {
                'correlativo': correlativo,
            }
            return HttpResponse(json.dumps(devolucion), content_type='application/json')
        else:
            return HttpResponse(json.dumps([{'Error':'No method get'}]), content_type='application/json')
    else:
        return redirect('login')

def view_get_correlativo_alfa(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
        if request.method =="GET":
            get_anio = str(datetime.datetime.now().year)[2:]
            lista_correlativos = Banco_alfa_new.objects.raw("select *  from ( 	select id_mensaje_a_n,substring( id_mensaje_a_n, 2, 4) as idnotam 	from aro_ais_notam_trafico_alfa_new 	where id_mensaje_a_n like %(anio)s 	union  	select id_mensaje_a_r,substring( id_mensaje_a_r, 2, 4) as idnotam 	from aro_ais_notam_trafico_alfa_repla 	where id_mensaje_a_r like %(anio)s 	union  	select id_mensaje_a_c,substring( id_mensaje_a_c, 2, 4)  as idnotam 	from aro_ais_notam_trafico_alfa_cancel 	where id_mensaje_a_c like %(anio)s ) as t_correlativo order by  idnotam desc limit 1" , { 'anio' : "%/"+get_anio} )
            if len(lista_correlativos) > 0:
                if len(str(int(lista_correlativos[0].idnotam)+1))==4:
                    correlativo = "A" + str(int(lista_correlativos[0].idnotam)+1) + "/" + get_anio
                if len(str(int(lista_correlativos[0].idnotam)+1))==3:
                    correlativo = "A0" + str(int(lista_correlativos[0].idnotam)+1) + "/" + get_anio
                if len(str(int(lista_correlativos[0].idnotam)+1))==2:
                    correlativo = "A00" + str(int(lista_correlativos[0].idnotam)+1) + "/" + get_anio
                if len(str(int(lista_correlativos[0].idnotam)+1))==1:
                    correlativo = "A000" + str(int(lista_correlativos[0].idnotam)+1) + "/" + get_anio
                
                
            else:
                correlativo = 'A0001/' + get_anio

            devolucion = {
                'correlativo': correlativo,
            }
            return HttpResponse(json.dumps(devolucion), content_type='application/json')
        else:
            return HttpResponse(json.dumps([{'Error':'No method get'}]), content_type='application/json')
    else:
        return redirect('login')

def view_get_aed_georef(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
        if request.method =="GET":
            
            lista_georeferencias = Aeropuerto.objects.raw( "(select aeropuerto, icao, fuente, geo_arp AS georef  from plan_vuelo_aeropuerto inner join (VALUES ('ARP')) AS t (fuente) on geo_arp not like %(nil)s ) union (select aeropuerto, icao, fuente, geo_vor AS georef from plan_vuelo_aeropuerto inner join (VALUES ('VOR')) AS t (fuente) on geo_vor not like %(nil)s)  union (select aeropuerto, icao, fuente, geo_ils AS georef from plan_vuelo_aeropuerto inner join (VALUES ('ILS')) AS t (fuente) on geo_ils not like %(nil)s)  union (select aeropuerto, icao, iata AS fuente, geo_arp AS georef from plan_vuelo_aeropuerto where iata like 'SLLF') order by icao" , { 'nil' : "NIL"} )
            
            lista_georeferencias = [ serializar_georef( geo ) for geo in lista_georeferencias ]

            devolucion = {
                'lista_georeferencias': lista_georeferencias,
            }
            return HttpResponse(json.dumps(devolucion), content_type='application/json')
        else:
            return HttpResponse(json.dumps([{'Error':'No method get'}]), content_type='application/json')
    else:
        return redirect('login')

def serializar_georef( geo ):
    return {
        'icao' : geo.icao,
        'fuente' : geo.fuente,
        'georef' : geo.georef,
    }

# AIM ################################################################################################################





########################### (FUENTE BANCO DE DATOS NOF) API PARA RECUPERAR DATOS DE NOTAM PASADO Y PASAR AL FORMYULARIO NOTAM ####################################3
def view_api_redirect_notam(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='TODOS_SERVICIOS').exists():
        # buscar notams
        get_codigo_notam = str(request.GET.get('codigo_notam')).upper()
        
        if "C" in get_codigo_notam:
            if Banco_charly_new.objects.filter(id_mensaje_c_n=get_codigo_notam).exists():
                notam_recuperado = Banco_charly_new.objects.get(id_mensaje_c_n=get_codigo_notam)
                return HttpResponse(json.dumps(segmentar_notam_charly(notam_recuperado)), content_type='application/json')
            else:
                if Banco_charly_repla.objects.filter(id_mensaje_c_r=get_codigo_notam).exists():
                    notam_recuperado = Banco_charly_repla.objects.get(id_mensaje_c_r=get_codigo_notam)
                    return HttpResponse(json.dumps(segmentar_notam_charly(notam_recuperado)), content_type='application/json')
                else:
                    if Banco_charly_cancel.objects.filter(id_mensaje_c_c=get_codigo_notam).exists():
                        notam_recuperado = Banco_charly_cancel.objects.get(id_mensaje_c_c=get_codigo_notam)
                        return HttpResponse(json.dumps(segmentar_notam_charly(notam_recuperado)), content_type='application/json')
        ####-------------------####-------------------####-------------------####-------------------####-------------------
        if "A" in get_codigo_notam:
            if Banco_alfa_new.objects.filter(id_mensaje_a_n=get_codigo_notam).exists():
                notam_recuperado = Banco_alfa_new.objects.get(id_mensaje_a_n=get_codigo_notam)
                return HttpResponse(json.dumps(segmentar_notam_alfa(notam_recuperado)), content_type='application/json')
            else:
                if Banco_alfa_repla.objects.filter(id_mensaje_a_r=get_codigo_notam).exists():
                    notam_recuperado = Banco_alfa_repla.objects.get(id_mensaje_a_r=get_codigo_notam)
                    return HttpResponse(json.dumps(segmentar_notam_alfa(notam_recuperado)), content_type='application/json')
                else:
                    if Banco_alfa_cancel.objects.filter(id_mensaje_a_c=get_codigo_notam).exists():
                        notam_recuperado = Banco_alfa_cancel.objects.filter(id_mensaje_a_c=get_codigo_notam)
                        return HttpResponse(json.dumps(segmentar_notam_alfa(notam_recuperado)), content_type='application/json')
        return HttpResponse(json.dumps({'error':"no encontrado"}), content_type='application/json')
    else:
        return redirect('login')



########################### (FUENTE AMHS) API PARA RECUPERAR DATOS DE NOTAM PASADO Y PASAR AL FORMYULARIO NOTAM ####################################3
def view_api_redirect_notam_amhs(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='TODOS_SERVICIOS').exists():
        # buscar notams
        get_codigo_notam = '('+ str(request.GET.get('codigo_notam')).upper()
        
        if "C" in get_codigo_notam:
            
            if Amhs_charly_new.objects.filter(idnotam__startswith=get_codigo_notam).exists():
                notam_recuperado = Amhs_charly_new.objects.filter(idnotam__startswith=get_codigo_notam).first()
                return HttpResponse(json.dumps(segmentar_notam_charly_amhs(notam_recuperado)), content_type='application/json')
            else:
                if Amhs_charly_repla.objects.filter(idnotam__startswith=get_codigo_notam).exists():
                    notam_recuperado = Amhs_charly_repla.objects.filter(idnotam__startswith=get_codigo_notam).first()
                    return HttpResponse(json.dumps(segmentar_notam_charly_amhs(notam_recuperado)), content_type='application/json')
                else:
                    if Amhs_charly_cancel.objects.filter(idnotam__startswith=get_codigo_notam).exists():
                        notam_recuperado = Amhs_charly_cancel.objects.filter(idnotam__startswith=get_codigo_notam).first()
                        return HttpResponse(json.dumps(segmentar_notam_charly_amhs(notam_recuperado)), content_type='application/json')
        ####-------------------####-------------------####-------------------####-------------------####-------------------
        if "A" in get_codigo_notam:
            if Amhs_alfa_new.objects.filter(idnotam__startswith=get_codigo_notam).exists():
                notam_recuperado = Amhs_alfa_new.objects.filter(idnotam__startswith=get_codigo_notam).first()
                return HttpResponse(json.dumps(segmentar_notam_alfa(notam_recuperado)), content_type='application/json')
            else:
                if Amhs_alfa_repla.objects.filter(idnotam__startswith=get_codigo_notam).exists():
                    notam_recuperado = Amhs_alfa_repla.objects.filter(idnotam__startswith=get_codigo_notam).first()
                    return HttpResponse(json.dumps(segmentar_notam_alfa(notam_recuperado)), content_type='application/json')
                else:
                    if Amhs_alfa_cancel.objects.filter(idnotam__startswith=get_codigo_notam).exists():
                        notam_recuperado = Amhs_alfa_cancel.objects.filter(idnotam__startswith=get_codigo_notam).first()
                        return HttpResponse(json.dumps(segmentar_notam_alfa(notam_recuperado)), content_type='application/json')
        return HttpResponse(json.dumps({'error':"no encontrado"}), content_type='application/json')
    else:
        return redirect('login')



def segmentar_notam_charly(notam):
    #########################################################################################################
    fir, codigo_q, tipo, nbo, alcance, niv_inf, niv_sup, coordenadas = notam.resumen.split(' ')[1].split('/')
    coordenadas, radio = coordenadas[:-3], coordenadas[-3:]
    #########################################################################################################
    recuperado = {
        'model_tiponotam' : notam.idnotam.split(' ')[1],
        'model_titulo_asunto' : codigo_q[1],
        'model_asunto' : codigo_q[1:3],
        'model_estado_asunto' : codigo_q[3:5],
        'model_tipo' : tipo,
        'model_nbo' : nbo,
        'model_alcance' : alcance,
        'nivel_inf' : niv_inf,
        'nivel_sup' : niv_sup,
        'model_coordenadas' : coordenadas,
        'radio' : radio,
        'lugar' : notam.aplica_a.split(' ')[1],
        'desde_fecha' : '20'+notam.valido_desde.split(" ")[1][0:6][0:2] +'-'+ notam.valido_desde.split(" ")[1][0:6][2:4] +'-'+  notam.valido_desde.split(" ")[1][0:6][4:6] ,
        'desde_hora' : notam.valido_desde.split(" ")[1][6:],
        'hasta_fecha' : '20'+notam.valido_hasta.split(" ")[1][0:6][0:2] +'-'+ notam.valido_hasta.split(" ")[1][0:6][2:4] +'-'+ notam.valido_hasta.split(" ")[1][0:6][4:6] ,
        'hasta_hora' : notam.valido_hasta.split(" ")[1][6:],
        'estimado' : notam.est,
        'permanente' : notam.perm,
        'pib_asunto': notam.asunto,
        'pib_estado_asunto': notam.estado_asunto,
        
    }
    if notam.valido_hasta:
        recuperado['hasta_fecha'] = '20'+notam.valido_hasta.split(" ")[1][0:6][0:2] +'-'+ notam.valido_hasta.split(" ")[1][0:6][2:4] +'-'+ notam.valido_hasta.split(" ")[1][0:6][4:6]
        recuperado['hasta_hora'] = notam.valido_hasta.split(" ")[1][6:]

    if len(notam.mensaje.split("D) ")) >= 2:
        casilla_d , casilla_e = notam.mensaje.split("D) ")[1].split("E) ")
        
    else:
        casilla_d = ""
        casilla_e = notam.mensaje.split("E) ")[1]

    cuerpo2 = casilla_e
    


    if len(cuerpo2.split("F) ")) >= 2:
        casilla_e , casilla_f = cuerpo2.split(" F) ")
        casilla_f, casilla_g = casilla_f.split("G) ")
        
    else:
        casilla_f = ''
        casilla_g= ""

    recuperado['casilla_d'] =casilla_d
    recuperado['cuerpo2'] = casilla_e

    recuperado['casilla_f'] =casilla_f
    recuperado['casilla_g'] =casilla_g
    return recuperado



def segmentar_notam_charly_amhs(notam):
    #########################################################################################################
    fir, codigo_q, tipo, nbo, alcance, niv_inf, niv_sup, coordenadas = notam.resumen.split(' ')[1].split('/')
    coordenadas, radio = coordenadas[:-4], coordenadas[-4:]
    #########################################################################################################
    recuperado = {
        'hora_deposito': notam.aftn2.split(' ')[0][2:],
        'fecha_deposito': str(notam.ingresado).split(' ')[0],
        'model_tiponotam' : notam.idnotam.split(' ')[1],
        'model_titulo_asunto' : codigo_q[1],
        'model_asunto' : codigo_q[1:3],
        'model_estado_asunto' : codigo_q[3:5],
        'model_tipo' : tipo,
        'model_nbo' : nbo,
        'model_alcance' : alcance,
        'nivel_inf' : niv_inf,
        'nivel_sup' : niv_sup,
        'model_coordenadas' : coordenadas,
        'radio' : radio,
        'lugar' : notam.aplica_a.split(' ')[1],
        'desde_fecha' : '20'+notam.valido_desde.split(" ")[1][0:6][0:2] +'-'+ notam.valido_desde.split(" ")[1][0:6][2:4] +'-'+  notam.valido_desde.split(" ")[1][0:6][4:6] ,
        'desde_hora' : notam.valido_desde.split(" ")[1][6:].replace(';;',''),
        'hasta_fecha':'',
        'hasta_hora':'',
        'casilla_f' : '',
        'casilla_g' : '',
        
    }

    if 'EST' in notam.valido_hasta:
        recuperado['estimado'] = True
    else:
        recuperado['estimado'] = False
    
    if 'PERM' in notam.valido_hasta:
        recuperado['permanente'] = True
    else:
        recuperado['permanente'] = False
    
    
    if notam.valido_hasta:
        recuperado['hasta_fecha'] = '20'+notam.valido_hasta.split(" ")[1][0:6][0:2] +'-'+ notam.valido_hasta.split(" ")[1][0:6][2:4] +'-'+ notam.valido_hasta.split(" ")[1][0:6][4:6]
        recuperado['hasta_hora'] = notam.valido_hasta.split(" ")[1][6:]

    if len(notam.mensaje.split("D) ")) >= 2:
        casilla_d , casilla_e = notam.mensaje.split("D) ")[1].split("E) ")
    else:
        casilla_d = ""
        casilla_e = notam.mensaje.split("E) ")[1]

    cuerpo2 = casilla_e
    


    if len(cuerpo2.split("F) ")) >= 2:
        casilla_e , casilla_f = cuerpo2.split(" F) ")
        casilla_f, casilla_g = casilla_f.split("G) ")
    else:
        casilla_f = ''
        casilla_g= ""

    recuperado['casilla_d'] =casilla_d
    recuperado['cuerpo2'] = casilla_e

    recuperado['casilla_f'] =casilla_f
    recuperado['casilla_g'] =casilla_g.replace(")","")

    return recuperado

def segmentar_notam_alfa(notam):
    return {
     'a':'a'   
    }
########################### API PARA RECUPERAR DATOS DE NOTAM PASADO Y PASAR AL FORMYULARIO NOTAM ####################################3
@login_required()
def view_estadistica_notam(request):
    areas = [
            {'data': estadisticas_charly_new(),
                'name': 'Charlie N'
            },

            {'data': estadisticas_alfa_new(),
                'name': 'Alpha N'
            }
        ]

    areas1 = [
        {'data': estadisticas_charly_repla(),
            'name': 'Charlie RPLC'
        },
        {'data': estadisticas_alfa_repla(),
            'name': 'Alpha RPLC'
        }
    ]
    areas2 = {
        "2013-02-10": 11,
        "2013-02-11": 6,
        "2013-02-12": 3,
        "2013-02-13": 2,
        "2013-02-14": 5, "2013-02-15": 3, "2013-02-16": 8, "2013-02-17": 6, "2013-02-18": 6, "2013-02-19": 12, "2013-02-20": 5, "2013-02-21": 5, "2013-02-22": 3, "2013-02-23": 1, "2013-02-24": 10, "2013-02-25": 1, "2013-02-26": 3, "2013-02-27": 2, "2013-02-28": 3, "2013-03-01": 2, "2013-03-02": 8}

    areas3 = {
        "2013-02-10": 11,
        "2013-02-11": 6,
        "2013-02-12": 3,
        "2013-02-13": 2,
        "2013-02-14": 5, "2013-02-15": 3, "2013-02-16": 8, "2013-02-17": 6, "2013-02-18": 6, "2013-02-19": 12, "2013-02-20": 5, "2013-02-21": 5, "2013-02-22": 3, "2013-02-23": 1, "2013-02-24": 10, "2013-02-25": 1, "2013-02-26": 3, "2013-02-27": 2, "2013-02-28": 3, "2013-03-01": 2, "2013-03-02": 8}
    return render(request, 'temp_plan_vuelo/temp_aro_ais/estadisticas_notam.html', locals())# ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )

def view_mapa_notam_search(request):
    return render(request, 'temp_plan_vuelo/temp_aro_ais/mapa_notam_search.html')# ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )

# API DE REVISAR QUE NO SE REPITA CORRELATIVO AL GUARDAR
@login_required()
def view_revisar_charly_antes_guardar(request):
    qs_charly_new = Banco_charly_new.objects.values('id_mensaje_c_n')
    qs_charly_new = [ notam['id_mensaje_c_n'] for notam in qs_charly_new ]

    qs_charly_repla = Banco_charly_repla.objects.values('id_mensaje_c_r')
    qs_charly_repla = [ notam['id_mensaje_c_r'] for notam in qs_charly_repla ]

    qs_charly_cancel = Banco_charly_cancel.objects.values('id_mensaje_c_c')
    qs_charly_cancel = [ notam['id_mensaje_c_c'] for notam in qs_charly_cancel ]

    qs_charly_new += qs_charly_repla + qs_charly_cancel

    get_correlativo = str(request.GET.get('charly_correlativo')).upper()

    if get_correlativo in qs_charly_new:
        return HttpResponse(json.dumps([{'repetido':True}]), content_type='application/json')
    else:
        return HttpResponse(json.dumps([{'repetido':False}]), content_type='application/json')

@login_required()
def view_revisar_alfa_antes_guardar(request):
    qs_alfa_new = Banco_alfa_new.objects.values('id_mensaje_a_n')
    qs_alfa_new = [ notam['id_mensaje_a_n'] for notam in qs_alfa_new ]

    qs_alfa_repla = Banco_alfa_repla.objects.values('id_mensaje_a_r')
    qs_alfa_repla = [ notam['id_mensaje_a_r'] for notam in qs_alfa_repla ]

    qs_alfa_cancel = Banco_alfa_cancel.objects.values('id_mensaje_a_c')
    qs_alfa_cancel = [ notam['id_mensaje_a_c'] for notam in qs_alfa_cancel ]

    qs_alfa_new += qs_alfa_repla + qs_alfa_cancel

    get_correlativo = str(request.GET.get('alfa_correlativo')).upper()

    if get_correlativo in qs_alfa_new:
        return HttpResponse(json.dumps([{'repetido':True}]), content_type='application/json')
    else:
        return HttpResponse(json.dumps([{'repetido':False}]), content_type='application/json')
# FIN DE LA API

    