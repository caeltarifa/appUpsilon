from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.contrib.auth.models import Group

import datetime

from django.db.models import Q
#from django.shortcuts import render_to_response


#from apps.plan_vuelo.forms import Vuelo_Aprobado_form, PostForm
from apps.plan_vuelo.models import Flp_trafico, EntrePuntos_flp,Ruta_flp, Trabajador
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
    if request.user.is_authenticated and request.user.groups.filter(name='CONTROLADORESLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and activo=true and empresa_institucion_id=1 order by apellido")
        return render(request, 'temp_plan_vuelo/index_coordinacion.html' ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
    else:
        return redirect('login')

def view_admin_coordinacion(request):
    controladores=Group.objects.get(name='CONTROLADORESLP')
    if request.user.is_authenticated and request.user.groups.filter(name='CONTROLADORESLP').exists():
        lista_fpl=Flp_trafico.objects.raw("select id_mensaje as id, id_mensaje, substring(id_mensaje, 1, 7) as id_amhs, substring(id_mensaje, 15,22) as fecha, substring(aftn2, 1,6) as hora_amhs, aftn1, aftn2, id_aeronave, reglas_vuelo, aeropuerto_salida, ruta, aeropuerto_destino, otros from plan_vuelo_flp_trafico order by id_amhs desc limit 90;")
        #id_mensaje, id_amhs, fecha, hora_amhs, aftn1, aftn2, id_aeronave, reglas_vuelo, aeropuerto_salida, ruta, aeropuerto_destino, otros
        #eliminando los planes de vuelo que no tengas IS
        
        #----metar=Metar_trafico.objects.raw("select * from plan_vuelo_metar_trafico order by fecha_llegada desc limit 100")

        #-----------------equipo_coordinacion = Trabajador.objects.raw("select * from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id)")

        return render(request, 'temp_plan_vuelo/progreso_vuelo.html', {'lista_fpl':lista_fpl} )#,'metar':metar} )
        #return render(request,'temp_plan_vuelo/admin.html')
    else:
        return redirect('login')

def view_aprobar_flp(request, id_plancompleto):
    if request.user.is_authenticated and request.user.is_active:        
        #plan_completo = Flp_trafico.objects.filter(id_mensaje=id_plancompleto)[0]
        if Flp_trafico.objects.filter(id_mensaje=id_plancompleto).exists():
            plan_completo = Flp_trafico.objects.filter(id_mensaje=id_plancompleto)
            fpl=plan_completo[0]
            context=serializar_fpl(plan_completo[0])

            lista_rutas,lista_rutas_puntos=Ruta_flp2.detectarRutas((fpl.ruta.split(' '))[1:])
            
            ficha={
                'avion':fpl.id_aeronave.split('-')[1],
                'velocidad':fpl.ruta.split(' ')[0].split('F')[0][1:],
                'nivel':fpl.ruta.split(' ')[0].split('F')[1],
                'origen':fpl.aeropuerto_salida[1:5],
                'salida':fpl.aeropuerto_salida[5:],
                'destino':fpl.aeropuerto_destino[1:5],
                'matricula':Ruta_flp2.getMatricula(fpl.otros),
                'transmision':Ruta_flp2.getTransmision(fpl.otros),
                #'ruta': lista_rutas,
                
                'rutas_detectadas': lista_rutas, #nombres de las rutas usadas
                'puntos_detectados': lista_rutas_puntos, #nombre de los puntos usados en las rutas
                
                'todaruta': Ruta_flp.objects.all(),
                'todopuntos': EntrePuntos_flp.objects.all(),
            }
            
            #context['id_mensaje']=EntrePuntos_flp.objects.all()
            
            context.update(ficha)

        else:
            context={
                'id_mensaje': 'NOT FOUND ERROR 404'
            }
        
        #obteniendo el cuerpo del plan de vuelo tipoavion, velocidad, nivel

        return render(request, 'temp_plan_vuelo/aprobar_plan.html', context ) #retorno el modal y el contexto
    else:
        return redirect('accounts/login/')
    




##VIEW FOR TO SEND DATA FOR THE TEMPLATE
import json
def view_update_flp (request):
    if request.user.is_authenticated and request.user.is_active:
        if request.is_ajax and request.method =="GET":
            lista_fpl=Flp_trafico.objects.raw("select id_mensaje, substring(id_mensaje, 1, 7) as id_amhs, substring(id_mensaje, 15,22) as fecha, substring(aftn2, 1,6) as hora_amhs, aftn1, aftn2, id_aeronave, reglas_vuelo, aeropuerto_salida, ruta, aeropuerto_destino, otros from plan_vuelo_flp_trafico order by id_amhs desc limit 90;")
            lista_fpl = [serializar_fpl(fpl) for fpl in lista_fpl]
            return HttpResponse(json.dumps(lista_fpl), content_type='application/json')
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


def view_identificacion(request, id_trabajador):
    if request.user.is_authenticated and request.user.is_active:        
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
    if request.user.is_authenticated and request.user.is_active:
        if request.is_ajax and request.method =="GET":
            cadena = request.GET.get('parametro')
            
            codigo_trabajador=cadena.split(":")[0]
            passwd=cadena.split(":")[1]

            persona=Trabajador.objects.filter(ci=codigo_trabajador)

            if persona.exists():
                if str(persona[0].codigo) in str(passwd):
                    return JsonResponse({'respuesta':True}, status=200)

        return JsonResponse({'respuesta':False}, status=200)
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
