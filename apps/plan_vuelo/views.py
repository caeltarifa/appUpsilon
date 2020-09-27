from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.contrib.auth.models import Group

import datetime
import json

from django.db.models import Q
#from django.shortcuts import render_to_response


#from apps.plan_vuelo.forms import Vuelo_Aprobado_form, PostForm
from apps.plan_vuelo.models import Flp_trafico, EntrePuntos_flp,Ruta_flp, Trabajador, Ruta_guardada, Flp_aprobado, Punto_satelital, Notam_trafico, Aeropuerto
Ruta_flp2=Ruta_flp()
EntrePuntos_flp2=EntrePuntos_flp()


# Create your views here.

def view_plan_vuelo(request):
    if request.user.is_authenticated:
        if request.user.is_active:
            return render(request, 'registration/already_logged.html')
        else:
            return redirect('view_admin_coordinacion')
    else:
        return redirect('login')

def view_panel_coordinacion(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='CONTROLADORESLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        return render(request, 'temp_plan_vuelo/index_coordinacion.html' ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
    else:
        return redirect('login')

def view_admin_coordinacion(request):
    controladores=Group.objects.get(name='CONTROLADORESLP')
    if request.user.is_authenticated and request.user.groups.filter(name='CONTROLADORESLP').exists():
        #lista_fpl=Flp_trafico.objects.raw("select id_mensaje as id, id_mensaje, substring(id_mensaje, 1, 7) as id_amhs, substring(id_mensaje, 15,22) as fecha, substring(aftn2, 1,6) as hora_amhs, aftn1, aftn2, id_aeronave, reglas_vuelo, aeropuerto_salida, ruta, aeropuerto_destino, otros from plan_vuelo_flp_trafico where aprobado=false order by id_mensaje asc limit 90;")
         
        now=datetime.datetime.now()
        dia = (str(now.day) if len(str(now.day))>1 else ('0' + str(now.day)))
        mesanio = ( str(now.month) if len(str(now.month))>1 else ('0'+str(now.month)) ) +  str(now.year)
        fecha_now = dia + mesanio
        
        dia = dia +"%"
        mesanio = "%"+mesanio
        lista_fpl=Flp_trafico.objects.raw("select id_mensaje, substring(id_mensaje, 1, 7) as id_amhs, substring(id_mensaje, 15,22) as fecha, substring(aftn2, 1,6) as hora_amhs, aftn1, aftn2, id_aeronave, reglas_vuelo, aeropuerto_salida, ruta, aeropuerto_destino, otros  from plan_vuelo_flp_trafico   where substring(aftn2,1,6) like %(dia)s  and substring(id_mensaje, 15,22) like %(mesanio)s   and  aprobado=false order by substring(aftn2, 1,6) desc limit 90;  " , {'dia':dia,'mesanio':mesanio})
        
        
        lista_fpl_hoy = []
        for fpl in lista_fpl:
            if fecha_now in fpl.id_mensaje:
                lista_fpl_hoy.append(fpl)
                
        lista_fpl_aprobado = Flp_trafico.objects.raw("select id_mensaje as id, id_mensaje, substring(id_mensaje, 1, 7) as id_amhs, substring(id_mensaje, 15,22) as fecha, substring(aftn2, 1,6) as hora_amhs, aftn1, aftn2, id_aeronave, reglas_vuelo, aeropuerto_salida, ruta, aeropuerto_destino, otros from plan_vuelo_flp_trafico where aprobado=true order by id_amhs desc limit 90;")

        #id_mensaje, id_amhs, fecha, hora_amhs, aftn1, aftn2, id_aeronave, reglas_vuelo, aeropuerto_salida, ruta, aeropuerto_destino, otros
        #eliminando los planes de vuelo que no tengas IS
        
        #----metar=Metar_trafico.objects.raw("select * from plan_vuelo_metar_trafico order by fecha_llegada desc limit 100")

        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")


        return render(request, 'temp_plan_vuelo/progreso_vuelo.html', {'lista_fpl':lista_fpl,'lista_fpl_hoy':lista_fpl_hoy ,'lista_fpl_aprobado':lista_fpl_aprobado , 'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
        #return render(request,'temp_plan_vuelo/admin.html')
    else:
        return redirect('login')




#######################   CONTROL DE APROBACION DE FPLs ##################
def view_aprobar_flp(request, id_plancompleto):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='CONTROLADORESLP').exists():        
        #plan_completo = Flp_trafico.objects.filter(id_mensaje=id_plancompleto)[0]
        if Flp_trafico.objects.filter(id_mensaje=str(id_plancompleto)).exists():
            plan_completo = Flp_trafico.objects.filter(id_mensaje=str(id_plancompleto))
            fpl=plan_completo[0]
            context=serializar_fpl(plan_completo[0])

            lista_rutas,lista_rutas_puntos=Ruta_flp2.detectarRutas(fpl.ruta.split(' ')[0:])
            
            ficha={
                'avion':fpl.id_aeronave.split('-')[1],
                'velocidad':fpl.ruta.split(' ')[0].split('F')[0][1:],
                'nivel':fpl.ruta.split(' ')[0].split('F')[1],
                'origen':fpl.aeropuerto_salida[1:5],
                'salida':fpl.aeropuerto_salida[5:],
                'destino':fpl.aeropuerto_destino[1:5],
                'matricula': fpl.id_aeronave.split('-')[1] if Ruta_flp2.getMatricula(fpl.otros)=='NFound' else Ruta_flp2.getMatricula(fpl.otros),
                'transmision':Ruta_flp2.getTransmision(fpl.otros),
                #'ruta': lista_rutas,
                
                'rutas_detectadas': lista_rutas, #nombres de las rutas usadas
                'puntos_detectados': lista_rutas_puntos, #nombre de los puntos usados en las rutas
                
                'todaruta': Ruta_flp.objects.all(),
                'todopuntos': EntrePuntos_flp.objects.all(),
            }
            
            #context['id_mensaje']=EntrePuntos_flp.objects.all()
            
            context.update(ficha)

            rutas_guardadas=Ruta_guardada.objects.filter(origen= ficha['origen'], destino=ficha['destino'], archivada=False)

            context.update({
                'rutas_guardadas':rutas_guardadas,
            })
            

        else:
            context={
                'id_mensaje': 'NOT FOUND ERROR 404'
            }
        
        equipo_activo = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and activo=true and empresa_institucion_id=1 order by activo")
        equipo_activo={
            'equipo_activo':equipo_activo,
            }
            
        context.update(equipo_activo)


        #obteniendo el cuerpo del plan de vuelo tipoavion, velocidad, nivel

        return render(request, 'temp_plan_vuelo/aprobar_plan.html', context  ) #retorno el modal y el contexto
    else:
        return redirect('accounts/login/')
    
def view_guardar_aprobacion(request):
    #cambia de estado en las rutas, dado un id_ruta para eliminar o archivar
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='CONTROLADORESLP').exists():
        response={
            'estado': 'NFound',
        }
        if request.is_ajax and request.method =="GET":
            get_id_fpl = request.GET.dict()['fpl']

            if Flp_trafico.objects.filter(id_mensaje=get_id_fpl).exists():
                get_tiempos = request.GET.dict()['tiempos']
                get_puntos = request.GET.dict()['puntos']
                get_rutas = request.GET.dict()['rutas']
                get_matricula = request.GET.dict()['matricula']
                get_nivel = request.GET.dict()['nivel']
                get_frecuencia = request.GET.dict()['frecuencia']
                get_ci = request.GET.dict()['persona']
                get_transponder = request.GET.dict()['transponder']

                if not Flp_trafico.objects.filter(id_mensaje=get_id_fpl)[0].aprobado:
                    objFpltrafico = Flp_trafico.objects.filter(id_mensaje=str(get_id_fpl) )[0]
                    objAprobado = Flp_aprobado(
                        id_flpaprobado = objFpltrafico,
                        controlador = Trabajador.objects.filter(ci=get_ci)[0],
                        transponder = int(get_transponder),
                        ruta_usada = get_rutas,
                        puntos_de_ficha = get_puntos,
                        matricula = get_matricula,
                        tiempos = get_tiempos,
                        frecuencias = get_frecuencia,
                        nivel = get_nivel,
                    )
                    objAprobado.save()

                    Flp_trafico.objects.filter(id_mensaje=get_id_fpl).update(aprobado=True)

                    response={
                        'estado': 'server200',
                    }
                else:
                    response={
                        'estado': 'server400',
                    }            
        return JsonResponse(response, status=200)
    else:
        return redirect('login')

def view_historial_aprobacion(request):
    #muestra las rutas guardas, archivadas y vigentes
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='CONTROLADORESLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")

        aprobados_historial = Flp_aprobado.objects.raw('select id_flpaprobado_id,id_aeronave,  aeropuerto_salida, aeropuerto_destino,fecha_aprobacion, hora_aprobacion, nombre, apellido from (select id_flpaprobado_id, id_aeronave, aeropuerto_salida, aeropuerto_destino,controlador_id,fecha_aprobacion, hora_aprobacion from plan_vuelo_flp_trafico inner join plan_vuelo_flp_aprobado on id_mensaje like id_flpaprobado_id) as t1 inner join plan_vuelo_trabajador on t1.controlador_id = plan_vuelo_trabajador.ci order by fecha_aprobacion, hora_aprobacion desc')
        #id_mensaje       | aeropuerto_salida | aeropuerto_destino  | fecha_aprobacion | hora_aprobacion | nombre  | apellido  

        return render(request, 'temp_plan_vuelo/fpl_aprobados_historial.html' ,{'equipo_trabajo': equipo_coordinacion, 'aprobados_historial': aprobados_historial } )#,'metar':metar} )
    else:
        return redirect('login')
#######################   CONTROL DE APROBACION DE FPLs ##################





##VIEW FOR TO SEND DATA FOR THE TEMPLATE

def view_update_flp (request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='CONTROLADORESLP').exists():
        if request.is_ajax and request.method =="GET":
            try:
                get_icao = request.GET.dict()['icao']
                get_icao = str(get_icao).replace('"',"")
            except:
                get_icao = ""
            
            now=datetime.datetime.now()
            dia = (str(now.day) if len(str(now.day))>1 else ('0' + str(now.day)))
            mesanio = ( str(now.month) if len(str(now.month))>1 else ('0'+str(now.month)) ) +  str(now.year)
            fecha_now = dia + mesanio
            
            dia = "25%"
            mesanio = "%092020"
            lista_fpl=Flp_trafico.objects.raw("select id_mensaje, substring(id_mensaje, 1, 7) as id_amhs, substring(id_mensaje, 15,22) as fecha, substring(aftn2, 1,6) as hora_amhs, aftn1, aftn2, id_aeronave, reglas_vuelo, aeropuerto_salida, ruta, aeropuerto_destino, otros  from plan_vuelo_flp_trafico   where substring(aftn2,1,6) like %(dia)s  and substring(id_mensaje, 15,22) like %(mesanio)s   and  aprobado=false order by substring(aftn2, 1,6) desc limit 90;  " , {'dia':dia,'mesanio':mesanio})

            if(len(get_icao)>0):
                lista_fpl_hoy = []
                for fpl in lista_fpl:
                    if get_icao in fpl.aeropuerto_destino.split(' ')[0]:
                        lista_fpl_hoy.append(fpl)
            else:
                
                lista_fpl_hoy = []
                for fpl in lista_fpl:
                    if fecha_now in fpl.id_mensaje:
                        lista_fpl_hoy.append(fpl)
            
            lista_fpl_hoy = [serializar_fpl_update(fpl) for fpl in lista_fpl_hoy]
            return HttpResponse(json.dumps(lista_fpl_hoy), content_type='application/json')
            #return HttpResponse({'lista_fpl':lista_fpl}, content_type='application/json')
        return JsonResponse({'respuesta':"ningun resultado"}, status=400)
    else:
        return redirect('accounts/login/')

def serializar_fpl(fpl):
    return {
        'id_mensaje':fpl.id_mensaje ,
        'aftn1':fpl.aftn1 ,
        'aftn2':fpl.aftn2 ,
        'id_aeronave':fpl.id_aeronave ,
        'reglas_vuelo':fpl.reglas_vuelo ,
        'aeropuerto_salida':fpl.aeropuerto_salida ,
        'rutafpl':fpl.ruta ,
        'aeropuerto_destino':fpl.aeropuerto_destino ,
        'otros':fpl.otros ,
    }
def serializar_fpl_update(fpl):
    return {
        'id_mensaje' : fpl.id_mensaje, 
        'id_amhs' : fpl.id_amhs, 
        'fecha' : fpl.fecha, 
        'hora_amhs' : fpl.hora_amhs, 
        'aftn1' : fpl.aftn1, 
        'aftn2' : fpl.aftn2, 
        'id_aeronave' : fpl.id_aeronave, 
        'reglas_vuelo' : fpl.reglas_vuelo, 
        'aeropuerto_salida' : fpl.aeropuerto_salida, 
        'ruta' : fpl.ruta, 
        'aeropuerto_destino' : fpl.aeropuerto_destino, 
        'otros' : fpl.otros,
    }

def view_update_notam_realtime(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='CONTROLADORESLP').exists():
        dic={ 'id_mensaje': False}
        if request.is_ajax and request.method =="GET":
            #notams recientes
            lista_notam = Notam_trafico.objects.filter(nuevo=True).only('id_mensaje','idnotam','resumen','ingresado')
            #id_mensaje       |    aftn1    |      aftn2      |          idnotam          |                    resumen                     | aplica_a | valido_desde  |    valido_hasta     |                   mensaje                    | nuevo |          ingresado 
            #lista_notam = [serializar_notam_realtime(notam) for notam in lista_notam]
            lista_notam2=[]
            for notam in lista_notam:
                hora,minuto,segundo = diferencie_entre_horas(notam.ingresado.replace(tzinfo=None) , datetime.datetime.now().replace(tzinfo=None) )
                if hora <= 5:
                    pasado=str(hora)+" horas y "+str(minuto) +" minutos."
                    lista_notam2.append( serializar_notam_realtime(notam,pasado) )

            return HttpResponse(json.dumps(lista_notam2), content_type='application/json')
            #return HttpResponse({'lista_fpl':lista_fpl}, content_type='application/json')
        return JsonResponse(dic, status=400)
    else:
        return redirect('accounts/login/')

def view_notam_modal(request, id_notam_mensaje):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='CONTROLADORESLP').exists():        
        #plan_completo = Flp_trafico.objects.filter(id_mensaje=id_plancompleto)[0]
        if Notam_trafico.objects.filter(id_mensaje=str(id_notam_mensaje)).exists():
            notam_completo = Notam_trafico.objects.filter(id_mensaje=str(id_notam_mensaje))[0]
        else:
            notam_completo = Notam_trafico

        return render(request, 'temp_plan_vuelo/modal_mensaje_completo.html', {'data': serializar_notam_completo(notam_completo) }  ) #retorno el modal y el contexto
    else:
        return redirect('accounts/login/')
    

def serializar_notam_completo(notam):
    return {
        'titulo': 'NOTAM',
        'id_mensaje' : notam.id_mensaje[0:7] + " " + notam.id_mensaje[7:13],
        'aftn1' : notam.aftn1,
        'aftn2' : notam.aftn2,
        'idnotam' : notam.idnotam,
        'resumen' : notam.resumen,
        'aplica_a' : notam.aplica_a,
        'valido_desde' : notam.valido_desde,
        'valido_hasta' : notam.valido_hasta,
        'mensaje' : notam.mensaje,
    }

def serializar_notam_realtime(notam, pasado):
    return {
        'id_mensaje' : notam.id_mensaje,
        'idnotam' : notam.idnotam,
        'resumen' : notam.resumen,
        'pasado' : pasado,
    }

def diferencie_entre_horas(data1, data2):
  #data1 = datetime.datetime.now()
  #data2 = datetime.datetime.now()
  diff = data2 - data1
  days, seconds = diff.days, diff.seconds
  hours = days * 24 + seconds // 3600
  minutes = (seconds % 3600) // 60
  seconds = seconds % 60
  return [hours,minutes,seconds]


#############################   CONTROL DE USUARIOS   #################################
def view_identificacion(request, id_trabajador):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='CONTROLADORESLP').exists():        
        if Trabajador.objects.filter(ci=int(id_trabajador)).exists():
            persona = Trabajador.objects.filter(ci=id_trabajador)[0]
            persona = {
                'nombre': persona.nombre,
                'apellido': persona.apellido, 
                'ci': persona.ci,
            }
        else:
            persona={
                'nombre': "Nfound",
                'apellido': "Nfound apellido",
            }
        
        return render(request, 'temp_plan_vuelo/modal_identificacion.html', {'persona': persona} ) #retorno el modal y el contexto
    else:
        return redirect('accounts/login/')

def view_validar_passwd(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='CONTROLADORESLP').exists():
        if request.is_ajax and request.method =="GET":
            cadena = request.GET.get('parametro')
            
            codigo_trabajador=cadena.split(":")[0]
            passwd=cadena.split(":")[1]

            persona=Trabajador.objects.filter(ci=codigo_trabajador)

            if persona.exists():
                if str(persona[0].codigo) in str(passwd):
                    persona=Trabajador.objects.get(ci=codigo_trabajador)
                    persona.activo=True
                    persona.save()
                    return JsonResponse({'respuesta':True}, status=200)

        return JsonResponse({'respuesta':False}, status=200)
    else:
        return redirect('accounts/login/')

def view_cerrar_sesion(request):
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='CONTROLADORESLP').exists():
        if request.is_ajax and request.method =="GET":
            carnet = request.GET.get('id_trabajador')
            
            persona=Trabajador.objects.filter(ci=carnet)

            if persona.exists():
                persona=Trabajador.objects.get(ci=carnet)
                persona.activo=False
                persona.save()
                return JsonResponse({'respuesta':True}, status=200)

        return JsonResponse({'respuesta':False}, status=200)
    else:
        return redirect('accounts/login/')
#############################   CONTROL DE USUARIOS   #################################





#############################   CONTROL DE RUTAS   #################################
def view_recordar_ruta(request):
    #muestra las rutas recordadas para un origen y destino dado 
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='CONTROLADORESLP').exists():
        dic={'estado':False}

        if request.is_ajax and request.method =="GET":
            getorigen = request.GET.dict()['origen']
            getdestino = request.GET.dict()['destino']
            getrutas = request.GET.dict()['rutas']
            getpuntos = request.GET.dict()['puntos']

            getrutas=getrutas[:len(getrutas)-1]
            getpuntos=getpuntos[:len(getpuntos)-1]

            consulta=Ruta_guardada.objects.filter(origen=getorigen, destino=getdestino,rutas = getrutas,puntos_limite = getpuntos)

            if not consulta.exists():
                objetoruta=Ruta_guardada(
                    origen = getorigen,
                    destino = getdestino,
                    rutas = getrutas,
                    puntos_limite = getpuntos
                )
                objetoruta.save()
                dic={'estado':True}
        
        return JsonResponse(dic, status=200)
    else:
        return redirect('accounts/login/')

def view_rutas_guardadas(request):
    #muestra las rutas guardas, archivadas y vigentes
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='CONTROLADORESLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")

        rutas_archivadas=Ruta_guardada.objects.filter(archivada=True)
        rutas_vigentes=Ruta_guardada.objects.filter(archivada=False)

        return render(request, 'temp_plan_vuelo/rutas_guardadas.html' ,{'equipo_trabajo': equipo_coordinacion, 'rutas_archivadas': rutas_archivadas, 'rutas_vigentes': rutas_vigentes,'todaruta': Ruta_flp.objects.all(),'todopuntos': EntrePuntos_flp.objects.all(),} )#,'metar':metar} )
    else:
        return redirect('login')

def view_restaurar_ruta(request):
    #cambia de estado en las rutas, dado un id_ruta para restaurar
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='CONTROLADORESLP').exists():
        response={
            'estado': False,
        }
        if request.is_ajax and request.method =="GET":
            getid_ruta = request.GET.dict()['ruta']
            if Ruta_guardada.objects.filter(id_ruta=getid_ruta).exists():
                Ruta_guardada.objects.filter(id_ruta=getid_ruta).update(archivada=False)
                response={
                    'estado': True,
                }            
        return JsonResponse(response, status=200)
    else:
        return redirect('login')

def view_archivar_ruta(request):
    #verificamos si el fpl no esta aprobado y luego guardamos
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='CONTROLADORESLP').exists():
        response={
            'estado': False,
        }
        if request.is_ajax and request.method =="GET":
            getid_ruta = request.GET.dict()['ruta']
            if Ruta_guardada.objects.filter(id_ruta=getid_ruta).exists():
                Ruta_guardada.objects.filter(id_ruta=getid_ruta).update(archivada=True)
                response={
                    'estado': True,
                }            
        return JsonResponse(response, status=200)
    else:
        return redirect('login')
#############################   CONTROL DE RUTAS   #################################






# VIEW_EJECUTIVO ################################################################################################################
def view_panel_ejecutivo(request):
    #muestra el panel principal ejecutivo
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='EJECUTIVOSLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        return render(request, 'temp_plan_vuelo/index_ejecutivo.html' ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
    else:
        return redirect('login')

#from traffic.data import airways

def view_carta_navegacional(request):
    #muestra el panel principal ejecutivo
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='EJECUTIVOSLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")

        puntos_satelitales = Punto_satelital.objects.raw('select * from plan_vuelo_punto_satelital')
        puntos_satelitales = [serializar_punto_satelital(punto) for punto in puntos_satelitales]

        return render(request, 'temp_plan_vuelo/temp_carta_navegacional/temp_carta_navegacional.html' ,{'equipo_trabajo': equipo_coordinacion , 'puntos_satelitales' : puntos_satelitales,'todaruta': Ruta_flp.objects.all()} )#,'metar':metar} )
    else:
        return redirect('login')

def serializar_punto_satelital(punto):
    return {
        'nombrepunto' : punto.nombrepunto,
        'latitude' : str(punto.latitude).replace(",","."),
        'longitude' : str(punto.longitude).replace(",","."),
    }


def view_obtener_dibujo_ruta(request):
    #muestra las rutas recordadas para un origen y destino dado 
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='EJECUTIVOSLP').exists():
        dic={'estado':False, 'lineas':[[{'longitude': 'null', 'latitude':'null'}]]}

        if request.is_ajax and request.method =="GET":
            get_vector_rutas = request.GET.dict()['seleccionados']
            get_vector_rutas = str(get_vector_rutas).split(',')

            #posiones=[{'longitude': longitude, 'latitude':latitude}]
            lineas=[]
            for rutax in get_vector_rutas:
                if rutax !='' and Ruta_flp.objects.filter(nombre_ruta=rutax).exists():
                    vector_puntos = Ruta_flp.objects.filter(nombre_ruta=rutax)[0].ruta.split(';;')
                    lineas.append(obterner_posiciones(vector_puntos))
                    dic={'estado':True, 'lineas':lineas,}
        return JsonResponse(dic, status=200)
    else:
        return redirect('accounts/login/')

def obterner_posiciones(vector_puntos):
    posiciones=[]
    for punto in vector_puntos:
        if Punto_satelital.objects.filter(nombrepunto=str(punto)).exists():
            x = Punto_satelital.objects.filter(nombrepunto=punto)[0]
            posiciones.append({
                'longitude': str(x.longitude).replace(",","."),
                'latitude': str(x.latitude).replace(",","."),
            })
    return posiciones





# VIEW_SUPERVISOR ################################################################################################################

# id_cargo |  nombre_cargo   | empresa_id
#----------+-----------------+------------
#        1 | COORDINADOR ACC |          1
#        2 | EJECUTIVO ACC   |          1
#        3 | SUPERVISOR ACC  |          1

def view_panel_supervisor(request):
    #muestra el panel principal ejecutivo
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='SUPERVISORESLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=3 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        return render(request, 'temp_plan_vuelo/index_supervisor.html' ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
    else:
        return redirect('login')

def view_servicio_met(request):
    #muestra el panel principal ejecutivo
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='SUPERVISORESLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=3 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        return render(request, 'temp_plan_vuelo/temp_servicio_met/servicio_met.html' ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
    else:
        return redirect('login')


from pyflightdata import FlightData
def view_aeropuertos_aeronaves(request):
    #muestra salidas y llegadas historial adenmas de de bucar todos los movimientos de la aeronave X
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='SUPERVISORESLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=3 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")

        api=FlightData()
        lista_llegadas=api.get_airport_arrivals('LPB',limit=25, earlier_data=True)

        #envia los aeropuertos y sus posiciones para el mapa
        diccionario={
            'type': 'Feature',
            'properties': {
                    'description':"vacio" ,
                    'iata':"vacio",
                    'icao': ''
                },
            'geometry': {
                    'type': 'Point',
                    'coordinates': ["vacio", "vacio"]
                }
            }

        dic={'estado':False, 'lista_fpl':[diccionario]}

        lista_aeropuerto=[]
        vector_aeropuertos = Aeropuerto.objects.all()
        for aero in  vector_aeropuertos:
            diccionario={
                'type': 'Feature',
                'properties': {
                        'nombre':aero.nombre ,
                        'iata':aero.iata,
                        'icao': aero.icao,
                    },
                'geometry': {
                        'type': 'Point',
                        'coordinates': [str(aero.longitude).replace(",","."), str(aero.latitude).replace(",",".") ]
                    }
                }
            lista_aeropuerto.append(json.dumps(diccionario))

        return render(request, 'temp_plan_vuelo/espacio_aereo.html' ,{'equipo_trabajo': equipo_coordinacion, 'lista_llegadas': lista_llegadas, 'lista_aeropuerto':lista_aeropuerto} )#,'metar':metar} )
    else:
        return redirect('login')


def view_enviar_fplaeropuerto(request):
    #envia planes de cuelo del aeropuerto x
    if request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name='EJECUTIVOSLP').exists():
        #envia los aeropuertos y sus posiciones para el mapa
        diccionario={
            'nombre': 'Feature',
            'properties': {
                    'description':"vacio" ,
                    'iata':"vacio",
                    'icao': ''
                },
            'geometry': {
                    'type': 'Point',
                    'coordinates': ["vacio", "vacio"]
                }
            }

        dic={'estado':False, 'lista_fpl':[diccionario]}

        if request.is_ajax and request.method =="GET":
            get_icao = request.GET.dict()['icao']

            lista_aeropuerto=[]
            if get_icao !='' and Aeropuerto.objects.filter(icao=get_icao).exists():
                vector_aeropuertos = Aeropuerto.objects.filter(icao=get_icao)
                for aero in  vector_aeropuertos:
                    diccionario={
                        'type': 'Feature',
                        'properties': {
                                'nombre':aero.nombre ,
                                'iata':aero.iata,
                                'icao': aero.icao,
                            },
                        'geometry': {
                                'type': 'Point',
                                'coordinates': [str(aero.longitude).replace(",","."), str(aero.latitude).replace(",",".") ]
                            }
                        }
                    lista_aeropuerto.append(diccionario)
                dic={'estado':True, 'lista_fpl':lista_aeropuerto,}
        return JsonResponse(dic, status=200)
    else:
        return redirect('accounts/login/')




#        '''
#        plan_vuelo=str(plan_completo.transponder+plan_completo.texto).split('-')
#
#        cadena=str(plan_completo.transponder+plan_completo.texto)
#        
#        velocidad,nivel=plan_vuelo[3][0:9].split('F')
#        ficha={'avion':plan_vuelo[1], 'velocidad':  plan_vuelo[3][0:5], 'nivel': plan_vuelo[3][6:9],'salida': plan_vuelo[4][4:9], 'origen': plan_completo.origen[1:5], 'destino': plan_vuelo[4][0:4], 'matricula':matricula, 'transmision':transmision }
#
#        #nivel,velocidad=plan_vuelo[3][0:9].split('F')
#        #ficha={
#        # 'avion':plan_vuelo[1], 
#        # 'velocidad': velocidad, 
#        # 'nivel': nivel, 
#        # 'salida': plan_vuelo[4][4:9], 
#        # 'origen': plan_completo.origen[1:5], 
#        # 'destino': plan_vuelo[4][0:4]
#        #  }
#
#        ruta=plan_vuelo[3].split(' ') #RUTA DEL AVION 
#        ruta.pop()
#        ruta.pop(0)
#
#        ruta=armarRuta(ruta)
#
#        todaruta=Ruta_flp.objects.all()
#        todopuntos=EntrePuntos_flp.objects.all()
#
#        context={
#            'aero': plan_completo.id_plan, #id_plan            , nombre de la aerolinea
#            'plan': str(plan_completo.transponder+'<br>'+plan_completo.texto), #Cuerpo del plan de vuelo
#            'ficha': ficha,  #envio de diccionario que contiene tipoavion velocidad niveldevuelo salidaaeropuerto
#            'ruta': ruta,
#            'todaruta': todaruta,
#            'todopuntos': todopuntos
#        }
#        '''








        # if EntrePuntos_flp.objects.filter(puntoInicial=punto).exists(): #pregunta si 'punto' existe en bolivia
        #     rutax.append(punto) #ARMA LA NUEVA RUTA
        # else:
        #     objRuta=Ruta_flp.objects.filter(nombre_ruta=punto)

        #     if objRuta.exists(): #pregunta si RUTA existe en bolivia
        #         if len(rutax)==0: #prgunto si el vector RUTAX sea distinto de vacio
        #             rutax.extend(identificarNumeros(objRuta[0].ruta.split(';;'))) #agrego vector_de_puntos a RUTAX e identificando el numeros enteros en la ruta
        #         else:
        #             rutaInvertida=invertirRuta( identificarNumeros(objRuta[0].ruta.split(';;')), rutax[-1] )
        #             rutax.pop()
        #             rutax.extend(rutaInvertida) #agrego vector_de_puntos a RUTAX , verificando si es necesario invertir la ruta e identificando el numeros enteros en la ruta
        #     elif punto.find('/')>=0:
        #         rutax.append(punto.split('/')[0])    

        #PARTE DEL ALGORITMO PARA ARMAR VECTOR DE RUTAS DEL FLP





# def view_form_plan_vuelo(request):
#     #form = Vuelo_Aprobado_form()
#     if request.method == 'POST':
#         form = Vuelo_Aprobado_form(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('temp_plan_vuelo/index.html')
#     return render(request, 'temp_plan_vuelo/form_vuelo_aprob.html', {'form':Vuelo_Aprobado_form.meta})

# def post_new(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post=form.save(commit=False)
#             post.author=request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#         else:
#             return render(request, 'temp_plan_vuelo/index.html',{'form':form})
#     else:
#         form=PostForm()
#         return render(request, 'temp_plan_vuelo/post_edit.html', {'form':form})

def post_detail(request, pk):
    post = get_object_or_404(Flp_trafico, pk=pk)
    return render(request, 'temp_plan_vuelo/post_detail.html',  {'post':post})

def view_template_prueba(request):
    if request.is_ajax and request.method =="GET":
        return JsonResponse({'valid':True}, status=200)

    return JsonResponse({}, status=400)

##VER TABLERO DESLIZABLE EN REACT JS

def view_tablero (request):
    return render(request, 'temp_plan_vuelo/tablero_trello.html')
