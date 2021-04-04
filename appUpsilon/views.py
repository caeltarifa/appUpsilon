from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from django.http import JsonResponse
from django.http import HttpResponse
import json
from datetime import datetime


from apps.plan_vuelo.models import Pib_tiempo_real
from apps.plan_vuelo.models import Notam_trafico_charly_new
from apps.plan_vuelo.models import Notam_trafico_charly_repla
from apps.plan_vuelo.models import Notam_trafico_charly_cancel

from apps.plan_vuelo.models import Notam_trafico_alfa_new
from apps.plan_vuelo.models import Notam_trafico_alfa_repla
from apps.plan_vuelo.models import Notam_trafico_alfa_cancel


from django.contrib.auth.models import Group

#from apps.plan_vuelo.forms import Vuelo_Aprobado_form, PostForm
from apps.plan_vuelo.models import Flp_trafico

# Create your views here.

# def view_modal_login(request):
#    if not request.user.is_authenticated:
#        redirect('login')
#    else:
#        redirect('view_pagina_principal')


def view_pagina_principal(request):

    # IMPORTANTE --- :user: adminupsilon pertenece a todos los grupos

    if request.user.is_authenticated:
        # preguntando si el 'usuario autenticado' pertenece al grupo de CONTROLADORES
        # if request.user.groups.filter(name='AROAISLP').exists():
        #    if request.user.username in 'aroaislp@aasana':
        #        return redirect('view_admin_ais')

        # preguntando si el 'usuario autenticado' pertenece al grupo de aerolineas
        if request.user.groups.filter(name='EMPRESASLP').exists():
            if request.user.username in 'AMASZONAS':
                return redirect('view_admin_amaszonas')

            if request.user.username in 'ECOJET':
                return redirect('view_admin_ecojet')

            if request.user.username in 'aviancalp@aasana':
                return redirect('view_admin_avianca')

        # preguntando si el 'usuario autenticado' pertenece al grupo de FELCN
        if request.user.groups.filter(name='FELCN').exists():
            if request.user.username in 'felcnlp@aasana':
                return redirect('view_admin_felcn')

        # preguntando si el 'usuario autenticado' pertenece al grupo de COMUNICACIONES
        if request.user.groups.filter(name='COMUNICACIONESLP').exists():
            if request.user.username in 'ccamlp@aasana':
                return redirect('view_admin_comunicaciones')

        if request.user.groups.filter(name='CONTROLADORESLP').exists():
            if request.user.username in 'acc_coordinacionlp@aasana':
                return redirect('view_panel_coordinacion')

        if request.user.groups.filter(name='EJECUTIVOSLP').exists():
            if request.user.username in 'acc_ejecutivolp@aasana':
                return redirect('view_panel_ejecutivo')

        if request.user.groups.filter(name='SUPERVISORESLP').exists():
            if request.user.username in 'acc_supervisorlp@aasana':
                return redirect('view_panel_supervisor')

        if request.user.groups.filter(name='AROAISLP').exists():
            if request.user.username in 'aroaislp@aasana':
                return redirect('view_panel_aroaislp')

        if request.user.groups.filter(name='AISNACIONAL').exists():
            if request.user.username in 'notaminternacional@aasana':
                return redirect('view_panel_notaminternacional')

        if request.user.groups.filter(name='INFORMACION_AERONAUTICA').exists():
            if request.user.username in 'aroaiscbba@aasana':
                return redirect('view_panel_aisslcb')

        # RETURN POR DEFECTO
        # ,'metar':metar} )
        return render(request, 'temp_plan_vuelo/prohibido.html')

    else:
        areas = [
            {'data': [
                ['2013-04-01 00:00:00 UTC', 52.9],
                ['2013-04-02 00:00:00 UTC', 57.9],
                ['2013-04-03 00:00:00 UTC', 65.9],
                ['2013-04-04 00:00:00 UTC', 75.9],
                ['2013-04-05 00:00:00 UTC', 55.9],
                ['2013-04-06 00:00:00 UTC', 45.9],
                ['2013-04-07 00:00:00 UTC', 65.9],
                ['2013-04-08 00:00:00 UTC', 85.7]
            ],
                'name': 'Recientes'
            },

            {'data': [
                ['2013-04-01 00:00:00 UTC', 42.9],
                ['2013-04-02 00:00:00 UTC', 73.9],
                ['2013-04-03 00:00:00 UTC', 55.9],
                ['2013-04-04 00:00:00 UTC', 65.9],
                ['2013-04-05 00:00:00 UTC', 35.9],
                ['2013-04-06 00:00:00 UTC', 75.9],
                ['2013-04-07 00:00:00 UTC', 55.9],
                ['2013-04-08 00:00:00 UTC', 25.7]
            ],
                'name': 'Antiguos'
            }
        ]

        areas1 = {
            "2013-02-10": 21,
            "2013-02-11": 26,
            "2013-02-12": 23,
            "2013-02-13": 22,
            "2013-02-14": 5, "2013-02-15": 3, "2013-02-16": 8, "2013-02-17": 6, "2013-02-18": 6, "2013-02-19": 12, "2013-02-20": 5, "2013-02-21": 5, "2013-02-22": 3, "2013-02-23": 1, "2013-02-24": 10, "2013-02-25": 1, "2013-02-26": 3, "2013-02-27": 2, "2013-02-28": 3, "2013-03-01": 2, "2013-03-02": 8}

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

        return render(request, 'registration/index_login.html', locals())


def view_panel_comunicaciones(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='COMUNICACIONESLP').exists():
        # ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
        return render(request, 'temp_plan_vuelo/index_comunicacion.html')
    else:
        return redirect('login')


def view_admin_comunicaciones(request):
    # def view_panel_coordinacion(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='COMUNICACIONESLP').exists():
        # ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
        return render(request, 'temp_plan_vuelo/index_coordinacion.html')
    else:
        return redirect('login')


# def control_acceso_login(request):
#     if request.user.is_authenticated or request.user.is_active:
#         view_pagina_principal(request)
#     else:
#         return render(request, 'registration/already_logged.html')
        # return redirect('accounts/login/')


# --------------------------- PIB EN TIEMPO REAL ----------------------------------
def convertir_fecha_pib(cadena):
    anio = cadena[0:2]
    mes = cadena[2:4]
    dia = cadena[4:6]
    hora = cadena[6:]
    if '01' in mes:
        mes = 'ENE'
    if '02' in mes:
        mes = 'FEB'
    if '03' in mes:
        mes = 'MAR'
    if '04' in mes:
        mes = 'ABR'
    if '05' in mes:
        mes = 'MAY'
    if '06' in mes:
        mes = 'JUN'
    if '07' in mes:
        mes = 'JUL'
    if '08' in mes:
        mes = 'AGO'
    if '09' in mes:
        mes = 'SEP'
    if '10' in mes:
        mes = 'OCT'
    if '11' in mes:
        mes = 'NOV'
    if '12' in mes:
        mes = 'DIC'
    formato_pib = dia + '/' + mes + '/' + anio + ' HR ' + hora
    return formato_pib


def serializar_pib(pib, tipo):
    desde = 'DESDE ' + convertir_fecha_pib(pib.desde)

    hasta = 'HASTA ' + convertir_fecha_pib(pib.hasta)
    if pib.perm:
        hasta = ''

    if pib.est:
        hasta = hasta + ' EST'

    return {
        'tipo': tipo,
        'lugar': pib.aplica_a[2:].strip(),
        'correlativo': "(" + pib.correlativo + ")",
        'referencia_notam': pib.referencia_notam,
        'desde': desde,
        'hasta':  hasta,
        'est': pib.est,
        'perm': pib.perm,
        'espaniol_decodificado': pib.espaniol_decodificado,
    }


def aun_es_valido(cadena):
    hora_cadena = cadena
    tiempo_notam = datetime.strptime(hora_cadena, '%y%m%d%H%M')
    ahora = datetime.now()

    if tiempo_notam >= ahora:
        return True
    else:
        return False


def eliminar_notam_del_pib(correlativo, tipo):
    Pib_tiempo_real.objects.filter(
        id_notam_pib__startswith='(C'+correlativo).delete()
    if 'NOTAMN' in tipo:
        Notam_trafico_charly_new.objects.filter(
            idnotam__startswith='(C'+correlativo).update(vigente=False)
    else:
        Notam_trafico_charly_repla.objects.filter(
            idnotam__startswith='(C'+correlativo).update(vigente=False)
    return False


def view_pib_tiempo_real(request):
    # lista de pib en notams nuevos
    lista_pib = Pib_tiempo_real.objects.raw("select id_notam_pib, correlativo, referencia_notam , desde, hasta, est, perm, espaniol_decodificado, hora_actualizacion, aplica_a from (select ptr.id_notam_pib, bnc.correlativo, bnc.referencia_notam , bnc.desde, bnc.hasta, bnc.est, bnc.perm, bnc.espaniol_decodificado, ptr.hora_actualizacion from plan_vuelo_pib_tiempo_real as ptr inner join aro_ais_banco_notam_charly as bnc on ptr.id_notam_pib like %(serie)s || bnc.correlativo || %(comodin)s and ptr.id_notam_pib not like %(notam)s order by ptr.hora_actualizacion desc ) as tabla_pib inner join plan_vuelo_notam_trafico_charly_new as tnew on tnew.idnotam like %(serie)s || tabla_pib.correlativo || %(comodin)s ", {
                                            'notam': '%NOTAMC%', 'serie': '(C', 'comodin': '%'})
    # lista de pib en notams replace
    lista_pib2 = Pib_tiempo_real.objects.raw("select id_notam_pib, correlativo, referencia_notam , desde, hasta, est, perm, espaniol_decodificado, hora_actualizacion, aplica_a from (select ptr.id_notam_pib, bnc.correlativo, bnc.referencia_notam , bnc.desde, bnc.hasta, bnc.est, bnc.perm, bnc.espaniol_decodificado, ptr.hora_actualizacion from plan_vuelo_pib_tiempo_real as ptr inner join aro_ais_banco_notam_charly as bnc on ptr.id_notam_pib like %(serie)s || bnc.correlativo || %(comodin)s and ptr.id_notam_pib not like %(notam)s order by ptr.hora_actualizacion desc ) as tabla_pib inner join plan_vuelo_notam_trafico_charly_repla as trepla on trepla.idnotam like %(serie)s || tabla_pib.correlativo || %(comodin)s ", {
                                             'notam': '%NOTAMC%', 'serie': '(C', 'comodin': '%'})

    if lista_pib[0].hora_actualizacion < lista_pib2[0].hora_actualizacion:
        lista_pib_ser = [{'hora_actualizado': str(
            lista_pib2[0].hora_actualizacion)}]
    else:
        lista_pib_ser = [{'hora_actualizado': str(
            lista_pib[0].hora_actualizacion)}]

    for x in lista_pib:
        if not x.perm:
            if aun_es_valido(x.hasta):
                lista_pib_ser.append(serializar_pib(x, 'NOTAMN'))
            else:
                # busco eliminarlo
                # elimino en la base: pib_tiempo_real
                # cambio a no vigente en la tabla charly_new
                if not x.est:
                    # si no es estimado, eliminacion sin piedad
                    eliminar_notam_del_pib(x.correlativo, 'NOTAMN')
        else:
            lista_pib_ser.append(serializar_pib(x, 'NOTAMN'))

    for x in lista_pib2:
        if not x.perm:
            if aun_es_valido(x.hasta):
                lista_pib_ser.append(serializar_pib(x, 'NOTAMR'))
            else:
                # busco eliminarlo
                # elimino en la base: pib_tiempo_real
                # cambio a no vigente en la tabla charly_new
                if not x.est:
                    # si no es estimado, eliminacion sin piedad
                    eliminar_notam_del_pib(x.correlativo, 'NOTAMR')
        else:
            lista_pib_ser.append(serializar_pib(x, 'NOTAMR'))

    return HttpResponse(json.dumps(lista_pib_ser), content_type='application/json')
    # return JsonResponse({'respuesta':"ningun resultado"}, status=200)

################################################################################################
################################################################################################
################################ API's PARA DEVOLVER HISTORIAL #################################
################################################################################################
################################################################################################


################################################################################################
############################ DESDE NOMTAM/ALFA DE NUEVO ####################################
def historico_alfa_from_notamn(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
        if request.method == "GET":
            #get_abreviatura = str(request.GET.dict()['abreviatura'])
            get_idnotam = str(request.GET.get('idnotam'))

            devolucion = {
                'abreviaturas': lista_abreviaturas,
            }

            return HttpResponse(json.dumps(devolucion), content_type='application/json')
        else:
            return HttpResponse(json.dumps([{'msj': 'error!'}]), content_type='application/json')
    return redirect('login')


################################################################################################
############################ DESDE NOMTAM/ALFA DE REEMPLAZO ####################################
def historico_alfa_from_notamr(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
        if request.method == "GET":
            #get_abreviatura = str(request.GET.dict()['abreviatura'])
            get_idnotam = str(request.GET.get('idnotam'))

            devolucion = {
                'abreviaturas': lista_abreviaturas,
            }

            return HttpResponse(json.dumps(devolucion), content_type='application/json')
        else:
            return HttpResponse(json.dumps([{'msj': 'error!'}]), content_type='application/json')
    return redirect('login')


################################################################################################
############################ DESDE NOMTAM/ALFA DE CANCEL #######################################
def historico_alfa_from_notamc(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
        if request.method == "GET":
            #get_abreviatura = str(request.GET.dict()['abreviatura'])
            get_idnotam = str(request.GET.get('idnotam'))

            devolucion = {
                'abreviaturas': lista_abreviaturas,
            }

            return HttpResponse(json.dumps(devolucion), content_type='application/json')
        else:
            return HttpResponse(json.dumps([{'msj': 'error!'}]), content_type='application/json')
    return redirect('login')



################################################################################################
################################################################################################


################################################################################################
############################ DESDE NOMTAM/CHARLY NUEVO #######################################
def historico_charly_from_notamn(request):
    if request.method == "GET":
        #get_abreviatura = str(request.GET.dict()['abreviatura'])
        get_idnotam = str(request.GET.get('idnotam'))

        devolucion = {
            'abreviaturas': lista_abreviaturas,
        }

        return HttpResponse(json.dumps(devolucion), content_type='application/json')
    else:
        return HttpResponse(json.dumps([{'msj': 'error!'}]), content_type='application/json')


################################################################################################
############################ DESDE NOMTAM/CHARLY REPLACE #######################################
def historico_charly_from_notamr(request):
    if request.method == "GET":
        #get_abreviatura = str(request.GET.dict()['abreviatura'])
        get_idnotam = str(request.GET.get('idnotam'))

        devolucion = {
            'abreviaturas': lista_abreviaturas,
        }

        return HttpResponse(json.dumps(devolucion), content_type='application/json')
    else:
        return HttpResponse(json.dumps([{'msj': 'error!'}]), content_type='application/json')


################################################################################################
############################ DESDE NOMTAM/CHARLY CANCEL #######################################
def historico_charly_from_notamc(request):
    if request.method == "GET":
        #get_abreviatura = str(request.GET.dict()['abreviatura'])
        get_idnotam = str(request.GET.get('idnotam'))

        devolucion = {
            'abreviaturas': lista_abreviaturas,
        }

        return HttpResponse(json.dumps(devolucion), content_type='application/json')
    else:
        return HttpResponse(json.dumps([{'msj': 'error!'}]), content_type='application/json')
