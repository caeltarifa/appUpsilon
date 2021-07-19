from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from django.http import JsonResponse
from django.http import HttpResponse
import json
from datetime import datetime


from apps.plan_vuelo.models import Pib_tiempo_real
from apps.plan_vuelo.models import Aeropuerto

from apps.plan_vuelo.models import Notam_trafico_charly_new
from apps.plan_vuelo.models import Notam_trafico_charly_repla
from apps.plan_vuelo.models import Notam_trafico_charly_cancel

from apps.plan_vuelo.models import Notam_trafico_alfa_new
from apps.plan_vuelo.models import Notam_trafico_alfa_repla
from apps.plan_vuelo.models import Notam_trafico_alfa_cancel



from django.contrib.auth.models import Group

# from apps.plan_vuelo.forms import Vuelo_Aprobado_form, PostForm
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
                ['2021-07-06 00:00:00 UTC', 52],
                ['2021-07-07 00:00:00 UTC', 57],
                ['2021-07-08 00:00:00 UTC', 65],
                ['2021-07-09 00:00:00 UTC', 75],
                ['2021-07-10 00:00:00 UTC', 55],
                ['2021-07-11 00:00:00 UTC', 45],
                ['2021-07-12 00:00:00 UTC', 65],
                ['2021-07-13 00:00:00 UTC', 85]
            ],
                'name': 'Charlie'
            },

            {'data': [
                ['2021-07-06 00:00:00 UTC', 42],
                ['2021-07-07 00:00:00 UTC', 73],
                ['2021-07-08 00:00:00 UTC', 55],
                ['2021-07-09 00:00:00 UTC', 65],
                ['2021-07-10 00:00:00 UTC', 35],
                ['2021-07-11 00:00:00 UTC', 75],
                ['2021-07-12 00:00:00 UTC', 55],
                ['2021-07-13 00:00:00 UTC', 25]
            ],
                'name': 'Alpha'
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
        
        #fecha_hora = {'anio': 11, 'mes': 12, 'dia':13}

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
    if cadena:
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
    else:
        return ""


def serializar_pib(pib, tipo):
    desde = 'DESDE ' + convertir_fecha_pib(pib.desde.split(' ')[1])


    if pib.perm:
        hasta = ''
    else:
        hasta = 'HASTA ' + convertir_fecha_pib(pib.hasta.split(' ')[1])

    if pib.est:
        hasta = hasta + ' EST'

    return {
        'tipo': tipo,
        'lugar': pib.aplica_a[2:].strip(),
        'correlativo': "(" + pib.correlativo + ")",
        'desde': desde,
        'hasta':  hasta,
        'est': pib.est,
        'perm': pib.perm,
        'espaniol_decodificado': pib.espaniol_decodificado,
        'asunto': pib.asunto,
    }


def aun_es_valido(cadena):
    hora_cadena = cadena.split(' ')[1]

    if hora_cadena:
        tiempo_notam = datetime.strptime(hora_cadena, '%y%m%d%H%M')
        ahora = datetime.now()

        if tiempo_notam >= ahora:
            return True
        else:
            return False
    return True


def eliminar_notam_del_pib(correlativo, tipo):
    Pib_tiempo_real.objects.filter(
        id_notam_pib__startswith='(C'+correlativo).delete()
    if 'NOTAMN' in tipo:
        Notam_trafico_charly_new.objects.filter(
            idnotam__startswith='(C'+correlativo).update(es_pib=False)
    else:
        Notam_trafico_charly_repla.objects.filter(
            idnotam__startswith='(C'+correlativo).update(vigente=False)
    return False


def view_pib_tiempo_real(request):
    # lista de pib en notams nuevos
    lista_pib = Pib_tiempo_real.objects.raw(" select 	id_notam_pib,	correlativo,	desde, 	hasta, 	tabla_pib.est, 	tabla_pib.perm, 	espaniol_decodificado,	hora_actualizacion, 	aplica_a,     tnew.asunto     from (	select		ptr.id_notam_pib, 		bnc.id_mensaje_c_n as correlativo, 		bnc.valido_desde as desde, 		bnc.valido_hasta as hasta, 		bnc.est, 		bnc.perm, 		bnc.pib_publicar as espaniol_decodificado, 		ptr.hora_actualizacion 	from 		plan_vuelo_pib_tiempo_real as ptr 	inner join 		aro_ais_notam_trafico_charly_new as bnc 	on 		ptr.id_notam_pib like %(parentesis)s || bnc.id_mensaje_c_n || %(comodin)s and 		ptr.id_notam_pib not like %(notam)s 	order by ptr.hora_actualizacion desc	) as tabla_pib inner join aro_ais_notam_trafico_charly_new as tnew on 	tnew.idnotam like %(parentesis)s || tabla_pib.correlativo || %(comodin)s AND tnew.es_pib=true", { 'notam': '%NOTAMC%', 'parentesis': '(', 'comodin': '%'})
    # lista de pib en notams replace

    lista_pib2 = Pib_tiempo_real.objects.raw("SELECT   	id_notam_pib, 	correlativo, 	desde,  	hasta,  	tabla_pib.est,  	tabla_pib.perm,  	espaniol_decodificado, 	hora_actualizacion,  	aplica_a,     trepla.asunto       FROM  ( 	SELECT   		ptr.id_notam_pib,  		bnc.id_mensaje_c_r as correlativo,  		bnc.valido_desde as desde,  		bnc.valido_hasta as hasta,  		bnc.est,  		bnc.perm,  		bnc.pib_publicar as espaniol_decodificado,  		ptr.hora_actualizacion  	FROM plan_vuelo_pib_tiempo_real AS ptr 	INNER JOIN  		aro_ais_notam_trafico_charly_repla AS bnc 	ON  		ptr.id_notam_pib like %(parentesis)s || bnc.id_mensaje_c_r || %(comodin)s AND  		ptr.id_notam_pib not like %(notam)s 	ORDER BY  		ptr.hora_actualizacion desc  ) AS tabla_pib INNER JOIN  	aro_ais_notam_trafico_charly_repla AS trepla ON  	trepla.idnotam like %(parentesis)s || tabla_pib.correlativo || %(comodin)s  AND trepla.es_pib=true", { 'notam': '%NOTAMC%', 'parentesis': '(', 'comodin': '%'})

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
################################################################################################
################################################################################################
# serializando .......


def serializar_notam(obj_not):
    if 'NOTAMC' in obj_not.idnotam:
        notamc = False
    else:
        notamc = obj_not.es_pib

    return {
        'aftn1': obj_not.aftn1,
        'aftn2': obj_not.aftn2,
        'idnotam': obj_not.idnotam,
        'resumen': obj_not.resumen,
        'aplica_a': obj_not.aplica_a,
        'valido_desde': obj_not.valido_desde,
        'valido_hasta': obj_not.valido_hasta,
        'mensaje': obj_not.mensaje,
        'es_pib': notamc,
        'ingresado': str(obj_not.ingresado),
    }

def serializar_notam_alfa(obj_not):
    return {
        'aftn1': obj_not.aftn1,
        'aftn2': obj_not.aftn2,
        'idnotam': obj_not.idnotam,
        'resumen': obj_not.resumen,
        'aplica_a': obj_not.aplica_a,
        'valido_desde': obj_not.valido_desde,
        'valido_hasta': obj_not.valido_hasta,
        'mensaje': obj_not.mensaje,
        'ingresado': str(obj_not.ingresado),
    }


def es_nuevo(cadena):
    if 'NOTAMN' in cadena:
        return True
    return False


def es_cancel(cadena):
    if 'NOTAMC' in cadena:
        return True
    return False


def es_replace(cadena):
    if 'NOTAMR' in cadena:
        return True
    return False

################################################################################################
################################################################################################
################################ API's PARA DEVOLVER HISTORIAL #################################
################################################################################################
################################################################################################


################################################################################################
############################ DESDE NOMTAM/ALFA NUEVO ####################################
def api_historico_alfa_from_notamn(request):
    # if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
    if request.method == "GET":
        # get_abreviatura = str(request.GET.dict()['abreviatura'])
        notam_nuevo = str(request.GET.get('idnotam')).upper()

        #notam_nuevo = '(A0227/21 NOTAMN'
        try:
            if len(notam_nuevo.split(' ')) ==2 and 'NOTAMN' in notam_nuevo:
                historico = Notam_trafico_alfa_new.objects.raw("drop table if exists t1; select alpha_historico_from_notamn('"+notam_nuevo +"') as vector into t1 ;  select talfa.id_mensaje_a_n, t1.vector  from t1, plan_vuelo_notam_trafico_alfa_new as talfa  limit 1;")[0].vector

                historico = historico.split(';')
                lista_notam_historico = []
                for x in historico:
                    if x:
                        if es_nuevo(x):
                            nuevo = Notam_trafico_alfa_new.objects.filter(
                                idnotam=x).first()
                            lista_notam_historico.append(serializar_notam_alfa(nuevo))
                        if es_replace(x):
                            repla = Notam_trafico_alfa_repla.objects.filter(
                                idnotam=x).first()
                            lista_notam_historico.append(serializar_notam_alfa(repla))
                        if es_cancel(x):
                            cancel = Notam_trafico_alfa_cancel.objects.filter(
                                idnotam=x).first()
                            lista_notam_historico.append(serializar_notam_alfa(cancel))

                devolucion = {
                    'lista_notam_historico': lista_notam_historico,
                }
                return HttpResponse(json.dumps(devolucion), content_type='application/json')
            else:
                return HttpResponse(json.dumps([{'Error en': notam_nuevo}]), content_type='application/json')
        except:
            return HttpResponse(json.dumps([{'Error en db': notam_nuevo}]), content_type='application/json')
    else:
        return HttpResponse(json.dumps([{'msj': "GET method no valid"}]), content_type='application/json')

    # return redirect('login')


################################################################################################
############################ DESDE NOMTAM/ALFA REEMPLAZO ####################################
def api_historico_alfa_from_notamr(request):
    #if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
    if request.method == "GET":
        # get_abreviatura = str(request.GET.dict()['abreviatura'])
        notam = str(request.GET.get('idnotam')).upper()
        #notam = '(A0271/21 NOTAMR A0191/21'
        try:
            if len(notam.split(' ')) == 3 and 'NOTAMR' in notam:
                lista_final=[]
                # extraccion hacia atras del notam
                historico = Notam_trafico_alfa_repla.objects.raw( "drop table if exists t1;  select alpha_historico_from_notamr2('"+notam+"') as vector into t1 ;  select talfa.id_mensaje_a_r, t1.vector  from t1, plan_vuelo_notam_trafico_alfa_repla as talfa  limit 1;" )[0].vector
                lista_final = historico.split(';')[::-1]

                # extraccion hacia adelante
                historico = Notam_trafico_alfa_repla.objects.raw( "drop table if exists t1;  select alpha_historico_from_notamr('"+notam+"') as vector into t1 ;  select talfa.id_mensaje_a_r, t1.vector  from t1, plan_vuelo_notam_trafico_alfa_repla as talfa  limit 1;" )[0].vector
                lista_final = lista_final + historico.split(';')


                lista_notam_historico=[]
                for x in lista_final:
                    if x:
                        if es_nuevo(x):
                            nuevo = Notam_trafico_alfa_new.objects.filter(idnotam=x).first()
                            lista_notam_historico.append(serializar_notam_alfa(nuevo))
                        if es_replace(x):
                            repla = Notam_trafico_alfa_repla.objects.filter(idnotam=x).first()
                            lista_notam_historico.append(serializar_notam_alfa(repla))
                        if es_cancel(x):
                            cancel = Notam_trafico_alfa_cancel.objects.filter(idnotam=x).first()
                            lista_notam_historico.append(serializar_notam_alfa(cancel))
                devolucion = {
                    'lista_notam_historico': lista_notam_historico,
                }
                return HttpResponse(json.dumps(devolucion), content_type='application/json')
            else:
                return HttpResponse(json.dumps([{'Error en': notam}]), content_type='application/json')
        except:
            return HttpResponse(json.dumps([{'Error en db': notam}]), content_type='application/json')
    else:
        return HttpResponse(json.dumps([{'msj': 'GET method no valid'}]), content_type='application/json')
    #return redirect('login')


################################################################################################
############################ DESDE NOMTAM/ALFA CANCEL #######################################
def api_historico_alfa_from_notamc(request):
    #if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
    if request.method == "GET":
        # get_abreviatura = str(request.GET.dict()['abreviatura'])
        notam = str(request.GET.get('idnotam')).upper()
        #notam = '(A0167/21 NOTAMC A0166/21'
        try:
            if len(notam.split(' ')) == 3 and 'NOTAMC' in notam:
                historico = Notam_trafico_alfa_new.objects.raw("drop table if exists t1; select alpha_historico_from_notamc('"+notam +
                                                    "') as vector into t1 ;  select talfa.id_mensaje_a_n, t1.vector  from t1, plan_vuelo_notam_trafico_alfa_new as talfa  limit 1;")[0].vector

                historico = historico.split(';')
                lista_notam_historico = []
                for x in historico:
                    if x:
                        if es_nuevo(x):
                            nuevo = Notam_trafico_alfa_new.objects.filter(idnotam=x).first()
                            lista_notam_historico.append(serializar_notam_alfa(nuevo))
                        if es_replace(x):
                            repla = Notam_trafico_alfa_repla.objects.filter(idnotam=x).first()
                            lista_notam_historico.append(serializar_notam_alfa(repla))
                        if es_cancel(x):
                            cancel = Notam_trafico_alfa_cancel.objects.filter(idnotam=x).first()
                            lista_notam_historico.append(serializar_notam_alfa(cancel))
                devolucion = {
                    'lista_notam_historico': lista_notam_historico,
                }
                return HttpResponse(json.dumps(devolucion), content_type='application/json')
            else:
                return HttpResponse(json.dumps([{'Error en': notam}]), content_type='application/json')
        except:
            return HttpResponse(json.dumps([{'Error en db': notam}]), content_type='application/json')
    else:
        return HttpResponse(json.dumps([{'msj': 'GET method no valid'}]), content_type='application/json')
    #return redirect('login')


################################################################################################
################################################################################################


################################################################################################
############################ DESDE NOMTAM/CHARLY NUEVO #######################################
def api_historico_charly_from_notamn(request):
    if request.method == "GET":
        # get_abreviatura = str(request.GET.dict()['abreviatura'])
        notam_nuevo = str(request.GET.get('idnotam')).upper()

        # notam_nuevo = '(C9990/21 NOTAMN'
        try:
            if len(notam_nuevo.split(' ')) == 2  and 'NOTAMN' in notam_nuevo:
                historico = Notam_trafico_charly_new.objects.raw("drop table if exists t1; select charlie_historico_from_notamn('"+notam_nuevo +
                                                                "') as vector into t1 ; select tcharly.id_mensaje_c_n, t1.vector from t1, plan_vuelo_notam_trafico_charly_new as tcharly limit 1; ")[0].vector

                historico = historico.split(';')
                lista_notam_historico = []
                for x in historico:
                    if x:
                        if es_nuevo(x):
                            nuevo = Notam_trafico_charly_new.objects.filter(
                                idnotam=x).first()
                            lista_notam_historico.append(serializar_notam(nuevo))
                        if es_replace(x):
                            repla = Notam_trafico_charly_repla.objects.filter(
                                idnotam=x).first()
                            lista_notam_historico.append(serializar_notam(repla))
                        if es_cancel(x):
                            cancel = Notam_trafico_charly_cancel.objects.filter(
                                idnotam=x).first()
                            lista_notam_historico.append(serializar_notam(cancel))

                devolucion = {
                    'lista_notam_historico': lista_notam_historico,
                }

                return HttpResponse(json.dumps(devolucion), content_type='application/json')
            else:
                return HttpResponse(json.dumps([{'Error en': notam_nuevo}]), content_type='application/json')
        except:
            return HttpResponse(json.dumps([{'Error en db': notam_nuevo}]), content_type='application/json')
    else:
        return HttpResponse(json.dumps([{'msj': 'error!'}]), content_type='application/json')


################################################################################################
############################ DESDE NOMTAM/CHARLY REPLACE #######################################
def api_historico_charly_from_notamr(request):
    if request.method == "GET":
        # get_abreviatura = str(request.GET.dict()['abreviatura'])
        notam = str(request.GET.get('idnotam')).upper()

        # notam = '(C9991/21 NOTAMR C9990/21'
        try:
            if notam and (len(notam.split(' ')) == 3) and 'NOTAMR' in notam:
                lista_final = []
                # extraccion hacia atras del notam
                historico = Notam_trafico_charly_repla.objects.raw("drop table if exists t1;  select charlie_historico_from_notamr2('"+notam +
                                                                "') as vector into t1 ;  select tcharly.id_mensaje_c_r, t1.vector  from t1, plan_vuelo_notam_trafico_charly_repla as tcharly  limit 1;")[0].vector
                lista_final = historico.split(';')[::-1]

                # extraccion hacia adelante
                historico = Notam_trafico_charly_repla.objects.raw("drop table if exists t1;  select charlie_historico_from_notamr('"+notam +
                                                                "') as vector into t1 ;  select tcharly.id_mensaje_c_r, t1.vector  from t1, plan_vuelo_notam_trafico_charly_repla as tcharly  limit 1;")[0].vector
                if len(historico.split(';')) > 1:
                    lista_final = lista_final + historico.split(';')[1:]

                lista_notam_historico = []
                for x in lista_final:
                    if x:
                        if es_nuevo(x):
                            nuevo = Notam_trafico_charly_new.objects.filter(
                                idnotam=x).first()
                            lista_notam_historico.append(serializar_notam(nuevo))
                        if es_replace(x):
                            repla = Notam_trafico_charly_repla.objects.filter(
                                idnotam=x).first()
                            lista_notam_historico.append(serializar_notam(repla))
                        if es_cancel(x):
                            cancel = Notam_trafico_charly_cancel.objects.filter(
                                idnotam=x).first()
                            lista_notam_historico.append(serializar_notam(cancel))

                devolucion = {
                    'lista_notam_historico': lista_notam_historico,
                }
                return HttpResponse(json.dumps(devolucion), content_type='application/json')
            else:
                return HttpResponse(json.dumps([{'Error en': notam}]), content_type='application/json')
        except:
            return HttpResponse(json.dumps([{'Error en db': notam}]), content_type='application/json')
    else:
        return HttpResponse(json.dumps([{'msj': 'GET METHOD NO VALID'}]), content_type='application/json')


################################################################################################
############################ DESDE NOMTAM/CHARLY CANCEL #######################################
def api_historico_charly_from_notamc(request):
    if request.method == "GET":
        # get_abreviatura = str(request.GET.dict()['abreviatura'])
        notam = str(request.GET.get('idnotam')).upper()

        # notam = '(C0295/21 NOTAMC C0292/21'
        #try:
        if notam and (len(notam.split(' ')) == 3) and 'NOTAMC' in notam:
            historico = Notam_trafico_charly_new.objects.raw("drop table if exists t1; select charlie_historico_from_notamc('"+notam +
                                                            "') as vector into t1 ; select talfa.id_mensaje_c_n, t1.vector from t1, plan_vuelo_notam_trafico_charly_new as talfa limit 1;")[0].vector
            historico = historico.split(';')
            lista_notam_historico = []
            for x in historico:
                if x:
                    if es_nuevo(x):
                        nuevo = Notam_trafico_charly_new.objects.filter(
                            idnotam=x).first()
                        lista_notam_historico.append(serializar_notam(nuevo))
                    if es_replace(x):
                        repla = Notam_trafico_charly_repla.objects.filter(
                            idnotam=x).first()
                        lista_notam_historico.append(serializar_notam(repla))
                    if es_cancel(x):
                        cancel = Notam_trafico_charly_cancel.objects.filter(
                            idnotam=x).first()
                        lista_notam_historico.append(serializar_notam(cancel))
            devolucion = {
                'lista_notam_historico': lista_notam_historico,
            }
            return HttpResponse(json.dumps(devolucion), content_type='application/json')
        else:
            return HttpResponse(json.dumps([{'Error en': notam}]), content_type='application/json')
        #except:
        #    return HttpResponse(json.dumps([{'Error en db': notam}]), content_type='application/json')
    else:
        return HttpResponse(json.dumps([{'msj': 'GET method no valid'}]), content_type='application/json')






def api_get_notam_aeropuerto(request):
    # if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='AISNACIONAL').exists():
    if request.method == "GET":
        # get_abreviatura = str(request.GET.dict()['abreviatura'])
        airport = str(request.GET.get('airport')).upper()
        try:
            if len(airport) <= 4 and ( Aeropuerto.objects.filter(icao=airport).exists() or 'SLLF' in airport) :
                lista_notam_charly = Notam_trafico_charly_new.objects.raw("select * from (select id_mensaje_c_n, split_part(idnotam, '/', 1) as correl, idnotam, resumen, aplica_a, valido_desde, valido_hasta, mensaje, ingresado from plan_vuelo_notam_trafico_charly_new where aplica_a like %(icao)s limit 20) as T_A union select *  from  (select id_mensaje_c_r, split_part(idnotam, '/', 1) as correl, idnotam, resumen, aplica_a, valido_desde, valido_hasta, mensaje, ingresado from plan_vuelo_notam_trafico_charly_repla where aplica_a like %(icao)s limit 20) AS T_B union select *  from  (select id_mensaje_c_c, split_part(idnotam, '/', 1) as correl, idnotam, resumen, aplica_a, valido_desde, valido_hasta, mensaje, ingresado from plan_vuelo_notam_trafico_charly_cancel where aplica_a like %(icao)s limit 20) AS T_C order by ingresado desc limit 20", {'icao':'%'+airport} )

                lista_notam_alfa = Notam_trafico_alfa_new.objects.raw("select * from (select id_mensaje_a_n, split_part(idnotam, '/', 1) as correl, idnotam, resumen, aplica_a, valido_desde, valido_hasta, mensaje, ingresado from plan_vuelo_notam_trafico_alfa_new where aplica_a like %(icao)s limit 20) as T_A union select *  from  (select id_mensaje_a_r, split_part(idnotam, '/', 1) as correl, idnotam, resumen, aplica_a, valido_desde, valido_hasta, mensaje, ingresado from plan_vuelo_notam_trafico_alfa_repla where aplica_a like %(icao)s limit 20) AS T_B union select *  from  (select id_mensaje_a_c, split_part(idnotam, '/', 1) as correl, idnotam, resumen, aplica_a, valido_desde, valido_hasta, mensaje, ingresado from plan_vuelo_notam_trafico_alfa_cancel where aplica_a like %(icao)s limit 20) AS T_C order by ingresado desc limit 20", {'icao':'%'+airport} )
                #####
                lista_notam_charly = [ serializarNotam(notam_c) for notam_c in lista_notam_charly ]
                lista_notam_alfa = [ serializarNotam(notam_a) for notam_a in lista_notam_alfa ]
                #####
                devolucion = {
                    'lista_notam_charly': lista_notam_charly,
                    'lista_notam_alfa': lista_notam_alfa,
                }
                return HttpResponse(json.dumps(devolucion), content_type='application/json')
            else:
                return HttpResponse(json.dumps([{'icao_error':airport}]), content_type='application/json')
                
        except:
            return HttpResponse(json.dumps([{'Error en db': airport}]), content_type='application/json')
    else:
        return HttpResponse(json.dumps([{'msj': "GET method no valid"}]), content_type='application/json')

def serializarNotam(notam):
    return {
        'correl' : notam.correl,
        'idnotam' : notam.idnotam,
        'resumen' : notam.resumen,
        'aplica_a' : notam.aplica_a,
        'valido_desde' : notam.valido_desde,
        'valido_hasta' : notam.valido_hasta,
        'mensaje' : notam.mensaje,
        'ingresado' : str(notam.ingresado),
    }




