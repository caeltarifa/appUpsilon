from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.contrib.auth.models import Group
import datetime
import json


# Create your views here.


from apps.plan_vuelo.models import  Notam_trafico, Trabajador
from apps.aro_ais.models import  Pib_trafico, Pib_extenso



# Create your views here.

def view_panel_aroais(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AROAISLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        return render(request, 'temp_plan_vuelo/temp_aro_ais/index_aroais.html' ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
    else:
        return redirect('login')

def view_pib_automatizado(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AROAISLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")

        lista_pib_pendiente = Pib_trafico.objects.raw("select * from aro_ais_pib_trafico inner join aro_ais_pib_extenso on ref_notam_amhs_id = notam_extenso_id and pendiente='t' ")
        lista_pib_archivado = Pib_trafico.objects.raw("select * from aro_ais_pib_trafico inner join aro_ais_pib_extenso on ref_notam_amhs_id = notam_extenso_id and archivado='t'  ")
        lista_pib_publicado = Pib_trafico.objects.raw("select * from aro_ais_pib_trafico inner join aro_ais_pib_extenso on ref_notam_amhs_id = notam_extenso_id and vigente='t' and msj_publicado!=''  ")
        # ref_notam_amhs_id | decodificado | publicado | vigente | archivado | oficialaro_id | pendiente   | msj_publicado |    notam_extenso_id    | notam_id |
        # notam_tipo | ref_notam_id | fir  | notam_codigo |  tipo_trafico  | proposito |    alcance    | fl_inferior | fl_superior | area |  
        # lugar   |      valid_desde       |      valid_hasta       |   agendado    | cuerpo | limit_superior | limit_inferior | indices_item_a |
        # indices_item_b | indices_item_c | indices_item_d | indices_item_e | indices_item_f | indices_item_g
        lista_pib_pendiente=[serializar_pibtrafico_pibextenso(pib) for pib in lista_pib_pendiente]
        lista_pib_archivado=[serializar_pibtrafico_pibextenso(pib) for pib in lista_pib_archivado]
        lista_pib_publicado=[serializar_pibtrafico_pibextenso(pib) for pib in lista_pib_publicado]
        

        equipo_activo = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and activo=true and empresa_institucion_id=1 order by activo")
        
        return render(request, 'temp_plan_vuelo/temp_aro_ais/notam_automatizado.html' ,{'equipo_activo':equipo_activo,'equipo_trabajo': equipo_coordinacion, 'lista_pendiente':lista_pib_pendiente, 'lista_archivado':lista_pib_archivado, 'lista_publicado':lista_pib_publicado, } )
    else:
        return redirect('login')



def serializar_pibtrafico_pibextenso(pibloong):
    if str(pibloong.decodificado).strip().index("E)") >0:
        decodificado=str(pibloong.decodificado).strip()[ str(pibloong.decodificado).strip().index("E)")+2 :-1 ] 
    else:
        decodificado=""
    return {
        'ref_notam_amhs_id' : str(pibloong.ref_notam_amhs_id).strip(),
        'decodificado' : decodificado,
        'publicado' : str(pibloong.publicado).strip(),
        'vigente' : str(pibloong.vigente).strip(),
        'archivado' : str(pibloong.archivado).strip(),
        'oficialaro_id' : str(pibloong.oficialaro_id).strip(),
        'pendiente' : str(pibloong.pendiente).strip(),
        'msj_publicado' : str(pibloong.msj_publicado).strip(),
        'notam_extenso_id' : str(pibloong.notam_extenso_id).strip(),
        'notam_id' : str(pibloong.notam_id).strip(),
        'notam_tipo' : str(pibloong.notam_tipo).strip(),
        'ref_notam_id' : str(pibloong.ref_notam_id).strip(),
        'fir' : str(pibloong.fir).strip(),
        'notam_codigo' : str(pibloong.notam_codigo).strip(),
        'tipo_trafico' : str(pibloong.tipo_trafico).strip(),
        'proposito' : str(pibloong.proposito).strip(),
        'alcance' : str(pibloong.alcance).strip(),
        'fl_inferior' : str(pibloong.fl_inferior).strip(),
        'fl_superior' : str(pibloong.fl_superior).strip(),
        'area' : str(pibloong.area).strip(),
        'lugar' : str(pibloong.lugar).strip(),
        'valid_desde' : str(pibloong.valid_desde).strip(),
        'valid_hasta' : str(pibloong.valid_hasta).strip(),
        'agendado' : str(pibloong.agendado).strip(),
        'cuerpo' : str(pibloong.cuerpo).strip(),
        'limit_superior' : str(pibloong.limit_superior).strip(),
        'limit_inferior' : str(pibloong.limit_inferior).strip(),
        'indices_item_a' : str(pibloong.indices_item_a).strip(),
        'indices_item_b' : str(pibloong.indices_item_b).strip(),
        'indices_item_c' : str(pibloong.indices_item_c).strip(),
        'indices_item_d' : str(pibloong.indices_item_d).strip(),
        'indices_item_e' : str(pibloong.indices_item_e).strip(),
        'indices_item_f' : str(pibloong.indices_item_f).strip(),
        'indices_item_g' :str(pibloong.indices_item_g).strip(),
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
                Pib_trafico.objects.filter(ref_notam_amhs_id=getid_mensaje).update(oficialaro_id=gettrabajador, msj_publicado=getpublicacion, pendiente=False, archivado=False, vigente=True, publicado=datetime.datetime.now())
                return JsonResponse({'estado':True}, status=200)

        return JsonResponse({'estado':False}, status=200)
    else:
        return redirect('accounts/login/')

    


def view_pib_tiemporeal(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AROAISLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")

        equipo_activo = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and activo=true and empresa_institucion_id=1 order by activo")
        
        return render(request, 'temp_plan_vuelo/temp_aro_ais/notam_realtime.html' ,{'equipo_activo':equipo_activo,'equipo_trabajo': equipo_coordinacion, } )
    else:
        return redirect('login')
    

def view_pibupdate_tiemporeal(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AROAISLP').exists():
        if request.is_ajax and request.method =="GET":
            getid_mensaje = request.GET.dict()['id_notam']

            lista_pib_publicado = Pib_trafico.objects.raw("select * from aro_ais_pib_trafico inner join aro_ais_pib_extenso on ref_notam_amhs_id = notam_extenso_id and vigente='t' and msj_publicado!=''  ")
            # ref_notam_amhs_id | decodificado | publicado | vigente | archivado | oficialaro_id | pendiente   | msj_publicado |    notam_extenso_id    | notam_id |
            # notam_tipo | ref_notam_id | fir  | notam_codigo |  tipo_trafico  | proposito |    alcance    | fl_inferior | fl_superior | area |  
            # lugar   |      valid_desde       |      valid_hasta       |   agendado    | cuerpo | limit_superior | limit_inferior | indices_item_a |
            # indices_item_b | indices_item_c | indices_item_d | indices_item_e | indices_item_f | indices_item_g
            lista_pib_publicado=[serializar_pibtrafico_pibextenso(pib) for pib in lista_pib_publicado]

            pib_Trafico=Pib_trafico.objects.filter(ref_notam_amhs_id=getid_mensaje)

            if pib_Trafico.exists():
                getpublicacion = request.GET.dict()['publicacion']
                gettrabajador = request.GET.dict()['persona']
                Pib_trafico.objects.filter(ref_notam_amhs_id=getid_mensaje).update(oficialaro_id=gettrabajador, msj_publicado=getpublicacion, pendiente=False, archivado=False, vigente=True, publicado=datetime.datetime.now())
                return JsonResponse({'estado':True}, status=200)

        return JsonResponse({'estado':False}, status=200)
    else:
        return redirect('accounts/login/')

