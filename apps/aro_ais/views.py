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


# Create your views here.


from apps.plan_vuelo.models import  Notam_trafico, Trabajador, Aeropuerto
from apps.aro_ais.models import  Pib_trafico, Pib_extenso, Pib_registro_documento
from apps.aro_ais.models import Abreviatura_8400

from apps.aro_ais.models import  Letra_asunto,Asunto,Estado_asunto

#from apps.aro_ais.models import  Simbolo_8400, Abreviatura_8400



from apps.trabajadoresATS.models import TrabajadoresATS, CuentasATS


#LIBRARY FOR CAST "['A','B','C']" TO  ['A','B','C'] (list element)
import ast
# Create your views here.

def view_panel_aroaislp(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AROAISLP').exists():
        #equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        return render(request, 'temp_plan_vuelo/temp_aro_ais/index_aroais.html')# ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
    else:
        return redirect('login')

def view_panel_notaminternacional(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AISNACIONAL').exists():
        return render(request, 'temp_plan_vuelo/temp_aro_ais/index_notaminternacional.html')
    else:
        return redirect('login')

def view_panel_serviciosaroais_aasana(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='INFORMACION_AERONAUTICA').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        return render(request, 'temp_plan_vuelo/temp_aro_ais/index_servicio_general_aroais.html' ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
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






def view_new_notam(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AISNACIONAL').exists():
        letra_asunto = Letra_asunto.objects.all().order_by('id_letra')
        #letra_asunto = [x.id_letra for x in letra_asunto]

        lista_letras = Letra_asunto.objects.all().order_by('id_letra')

        return render(request, 'temp_plan_vuelo/temp_aro_ais/new_notam.html', {'vec_letra': letra_asunto, 'lista_letras': lista_letras})
    else:
        return redirect('login')

def view_replace_notam(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AISNACIONAL').exists():
        letra_asunto = Letra_asunto.objects.all().order_by('id_letra')
        #letra_asunto = [x.id_letra for x in letra_asunto]
        return render(request, 'temp_plan_vuelo/temp_aro_ais/replace_notam.html', {'vec_letra': letra_asunto})
    else:
        return redirect('login')

def view_cancel_notam(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AISNACIONAL').exists():
        letra_asunto = Letra_asunto.objects.all().order_by('id_letra')
        #letra_asunto = [x.id_letra for x in letra_asunto]
        return render(request, 'temp_plan_vuelo/temp_aro_ais/cancel_notam.html', {'vec_letra': letra_asunto})
    else:
        return redirect('login')

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
   
        #lista_notams_recientes=[serializar_notam(notamx) for notamx in lista_notams_recientes]

        lista_notam_charly = []
        lista_notam_alfa = []
        
        for notam in lista_notams_recientes:
            if '(C' in notam.idnotam:
                lista_notam_charly.append(serializar_notam(notam))
            else:
                lista_notam_alfa.append(serializar_notam(notam))
        
        return render(request, 'temp_plan_vuelo/temp_aro_ais/lista_notam.html' ,{'lista_notam_charly':lista_notam_charly, 'lista_notam_alfa':lista_notam_alfa} )
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
            
            inf_constante = {
                'post_amhs1' : str(request.POST.get('amhs1')),
                'post_amhs2' : str(request.POST.get('amhs2')),
                'post_resumen' : str(request.POST.get('resumen')),
                'post_aplica_a' : str(request.POST.get('aplica_a')),
                'post_valido_desde' : str(request.POST.get('valido_desde')),
                'post_valido_hasta' : str(request.POST.get('valido_hasta')),
                'post_mensaje' : str(request.POST.get('mensaje')),
                'post_asunto' : str(request.POST.get('asunto')),
                'post_estado_asunto' : str(request.POST.get('estado_asunto')),
                'post_estimado' : str(request.POST.get('estimado')),
                'post_permanente' : str(request.POST.get('permanente')),
            }

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



            ############ CONTROL DE ID_NOTAM           
            if id_charly:
                if 'NOTAMN' in post_tipo:
                    guardar_nuevo_charly(id_charly, inf_constante, post_pib_publicar)

                #if 'NOTAMR' in post_tipo:
                #    guardar_repla_charly(id_mensaje, charly, inf_constante, post_pib_publicar)
#
                #if 'NOTAMC' in post_tipo:
                #    guardar_cancel_charly(id_mensaje, charly, inf_constante)

            
            if id_alfa:
                if 'NOTAMN' in post_tipo:
                    guardar_nuevo_alfa(id_alfa, inf_constante)

                #if 'NOTAMR' in post_tipo:
                #    guardar_repla_alfa(id_mensaje, alfa, inf_constante)
#
                #if 'NOTAMC' in post_tipo:
                #    guardar_cancel_alfa(id_mensaje, alfa, inf_constante)
            
            
            ############ CONTROL DE ID_NOTAM           

            #return render(request, 'temp_ais_nacional/blanco.html',{'devolucion':devolucion})
            return HttpResponseRedirect(reverse( view_pagina_principal ))
        else:
            return render(request, 'temp_plan_vuelo/temp_aro_ais/new_notam.html' , locals())
            #return HttpResponse(json.dumps([{'Response':'Envie datos validos.'}]), content_type='application/json')
    else:
        return redirect('login')


## FUNCIONES PARA GUARDAR NOTAM CLASIFICADO
def guardar_nuevo_charly(id_charly, inf_constante, post_pib_publicar):
    banco_charly=Banco_charly_new()

    banco_charly.id_mensaje_c_n = id_charly
    banco_charly.aftn1 = inf_constante['post_amhs1']
    banco_charly.aftn2 = inf_constante['post_amhs2']
    banco_charly.idnotam = '(' +id_charly + ' NOTAMN'
    banco_charly.resumen = inf_constante['post_resumen']
    banco_charly.aplica_a = inf_constante['post_aplica_a']
    banco_charly.valido_desde = inf_constante['post_valido_desde']
    banco_charly.valido_hasta = inf_constante['post_valido_hasta']
    banco_charly.mensaje = inf_constante['post_mensaje']

    if 'EST' in inf_constante['post_estimado']:
        banco_charly.est = True
    if 'PERM' in inf_constante['post_permanente']:
        banco_charly.perm = True

    banco_charly.es_pib = True

    banco_charly.asunto = inf_constante['post_asunto']
    banco_charly.estado_asunto = inf_constante['post_estado_asunto']

    banco_charly.pib_publicar = post_pib_publicar

    banco_charly.save()
'''
def guardar_repla_charly(id_mensaje, charly, inf_constante, post_pib_publicar):
    banco_charly=Banco_charly_repla()

    banco_charly.id_mensaje_c_r = id_mensaje
    banco_charly.aftn1 = inf_constante['post_amhs1']
    banco_charly.aftn2 = inf_constante['post_amhs2']
    banco_charly.idnotam = charly + ' NOTAMR'
    banco_charly.resumen = inf_constante['post_resumen']
    banco_charly.aplica_a = inf_constante['post_aplica_a']
    banco_charly.valido_desde = inf_constante['post_valido_desde']
    banco_charly.valido_hasta = inf_constante['post_valido_hasta']
    banco_charly.mensaje = inf_constante['post_mensaje']

    banco_charly.es_pib = True

    banco_charly.asunto = inf_constante['post_asunto']
    banco_charly.estado_asunto = inf_constante['post_estado_asunto']

    banco_charly.pib_publicar = post_pib_publicar

    banco_charly.save()
'''

#def guardar_cancel_charly(id_mensaje, alfa, inf_constante):
#######
def guardar_nuevo_alfa(id_alfa, inf_constante):
    banco_alfa=Banco_alfa_new()

    banco_alfa.id_mensaje_a_n = id_alfa
    banco_alfa.aftn1 = inf_constante['post_amhs1']
    banco_alfa.aftn2 = inf_constante['post_amhs2']
    banco_alfa.idnotam = '('+id_alfa + ' NOTAMN'
    banco_alfa.resumen = inf_constante['post_resumen']
    banco_alfa.aplica_a = inf_constante['post_aplica_a']
    banco_alfa.valido_desde = inf_constante['post_valido_desde']
    banco_alfa.valido_hasta = inf_constante['post_valido_hasta']
    banco_alfa.mensaje = inf_constante['post_mensaje']

    if inf_constante['post_estimado']:
        banco_alfa.est = True
    if inf_constante['post_permanente']:
        banco_alfa.perm = True

    banco_alfa.asunto = inf_constante['post_asunto']
    banco_alfa.estado_asunto = inf_constante['post_estado_asunto']

    banco_alfa.save()

'''
def guardar_repla_alfa(id_mensaje, alfa, inf_constante):

def guardar_cancel_alfa(id_mensaje, alfa, inf_constante):
'''

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
                correlativo = "A" + str(int(lista_correlativos[0].idnotam)+1) + "/" + get_anio
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

# AIM ################################################################################################################
