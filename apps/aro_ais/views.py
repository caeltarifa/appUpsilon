from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.contrib.auth.models import Group
import datetime
import json


# Create your views here.


from apps.plan_vuelo.models import  Notam_trafico, Trabajador, Aeropuerto
from apps.aro_ais.models import  Pib_trafico, Pib_extenso, Pib_registro_documento


from apps.trabajadoresATS.models import TrabajadoresATS, CuentasATS


#LIBRARY FOR CAST "['A','B','C']" TO  ['A','B','C'] (list element)
import ast
# Create your views here.

def view_panel_aroais(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AROAISLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        return render(request, 'temp_plan_vuelo/temp_aro_ais/index_aroais.html' ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
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






def view_pib_automatizado(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AROAISLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")

        lista_pib_pendiente = Pib_trafico.objects.raw("select * from (select * from aro_ais_pib_trafico inner join aro_ais_pib_extenso on ref_notam_amhs_id = notam_extenso_id and pendiente='t') as pib inner join plan_vuelo_notam_trafico on id_mensaje=ref_notam_amhs_id order by DATE(ingresado) desc;")
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
        
        equipo_activo = Trabajador.objects.raw("select ci, nombre, apellido, activo  from plan_vuelo_trabajador where activo='t' and ci in ( select trabajador_id from plan_vuelo_trabajador_cargo where cargo_id in ( select id_cargo  from plan_vuelo_cargo where cuenta_usuario_id in  (select id from auth_user where username like %(usuario)s) ) )", {'usuario':request.user.username})
        
        return render(request, 'temp_plan_vuelo/temp_aro_ais/notam_automatizado.html' ,{'equipo_activo':equipo_activo,'equipo_trabajo': equipo_coordinacion, 'lista_pendiente':lista_pib_pendiente, 'lista_archivado':lista_pib_archivado, 'lista_publicado':lista_pib_publicado, 'lista_notam':lista_notams_recientes} )
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
        lista_pib_pendiente = Pib_trafico.objects.raw("select * from aro_ais_pib_trafico inner join aro_ais_pib_extenso on ref_notam_amhs_id = notam_extenso_id and pendiente='t' ")
        lista_pib_archivado = Pib_trafico.objects.raw("select * from aro_ais_pib_trafico inner join aro_ais_pib_extenso on ref_notam_amhs_id = notam_extenso_id and archivado='t'  ")
        lista_pib_publicado = Pib_trafico.objects.raw("select * from aro_ais_pib_trafico inner join aro_ais_pib_extenso on ref_notam_amhs_id = notam_extenso_id and vigente='t' and msj_publicado!=''  ")
        lista_notams_recientes=Notam_trafico.objects.all().order_by('-ingresado')[:100]

        # ref_notam_amhs_id | decodificado | publicado | vigente | archivado | oficialaro_id | pendiente   | msj_publicado |    notam_extenso_id    | notam_id |
        # notam_tipo | ref_notam_id | fir  | notam_codigo |  tipo_trafico  | proposito |    alcance    | fl_inferior | fl_superior | area |  
        # lugar   |      valid_desde       |      valid_hasta       |   agendado    | cuerpo | limit_superior | limit_inferior | indices_item_a |
        # indices_item_b | indices_item_c | indices_item_d | indices_item_e | indices_item_f | indices_item_g
        lista_pib_pendiente=[serializar_pibtrafico_pibextenso(pib) for pib in lista_pib_pendiente]
        lista_pib_archivado=[serializar_pibtrafico_pibextenso(pib) for pib in lista_pib_archivado]
        lista_pib_publicado=[serializar_pibtrafico_pibextenso(pib) for pib in lista_pib_publicado]
        lista_notams_recientes=[serializar_notam(notamx) for notamx in lista_notams_recientes]

        #equipo_activo = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and activo=true and empresa_institucion_id=1 order by activo")
        
        return render(request, 'temp_plan_vuelo/temp_aro_ais/lista_notam.html' ,{'lista_notam':lista_notams_recientes} )
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

                SLAP
                SLAS
                SLBN
                SLBJ
                Cruz
                SLCN
                SLHI
                SLCO
                SLCB
                SLCP
                SLCC
                SLAG
                SLGY
                SLLP
                SLLJ
                SLMG
                SLOR
                SLPO
                SLPR
                SLPS
                SLRY
                SLRI
                SLRB
                SLRQ
                SLSB
                SLSM
                SLSI
                SLJV
                SLJO
                SLJE
                SLTI
                SLRA
                SLSA
                SLET
                SLVR
                SLSU
                SLTJ
                SLTR
                SLUY
                SLVG
                SLVM
                SLTL
                SLYA
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
