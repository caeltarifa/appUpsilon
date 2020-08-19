from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.models import Group

import datetime

from django.db.models import Q
from django.shortcuts import render_to_response


#from apps.plan_vuelo.forms import Vuelo_Aprobado_form, PostForm
from apps.plan_vuelo.models import Flp_trafico, Metar_trafico, EntrePuntos_flp,Ruta_flp
# Create your views here.

def view_plan_vuelo(request):
    if request.user.is_authenticated:

        if request.user.is_active:
            return render(request, 'registration/already_logged.html')
        else:
            return redirect('view_admin')
    else:
        return redirect('login')

def view_admin(request):
    controladores=Group.objects.get(name='CONTROLADORES')
    if request.user.is_authenticated and request.user.groups.filter(name='CONTROLADORES').exists():
        ###post=Flp_trafico.objects.raw("select * from plan_vuelo_Flp_trafico where CAST(fecha_llegada AS date) = CAST('2019-10-11' AS date)");
        ###post=Flp_trafico.objects.raw("select id, hora_amhs, prioridad, origen, id_plan from plan_vuelo_flp_trafico where hora_amhs like '"+str(datetime.datetime.now().day)+"%%%%' order by id_amhs desc limit 100")
        
        post=Flp_trafico.objects.raw("select * from plan_vuelo_flp_trafico where id_plan like '%%-%%' order by hora_amhs desc limit 100")
        #post=Flp_trafico.objects.raw("select distinct on(no_dupli.id_amhs) total.id,total.id_amhs,total.fecha_llegada,total.hora_amhs,total.prioridad,total.id_plan,total.transponder,total.origen,total.texto from (select id_amhs as x ,id,id_amhs,fecha_llegada,hora_amhs,prioridad,id_plan,transponder,origen,texto from plan_vuelo_flp_trafico) as total, plan_vuelo_flp_trafico as no_dupli where x like no_dupli.id_amhs limit 85")

        metar=Metar_trafico.objects.raw("select * from plan_vuelo_metar_trafico order by fecha_llegada desc limit 100")
        return render(request, 'temp_plan_vuelo/admin.html', {'post':post,'metar':metar} )
        #return render(request,'temp_plan_vuelo/admin.html')
    else:
        return redirect('login')

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






def invertirRuta(vector,punto):
    try:
        indice = vector.index(punto)
        mitad= int(len(vector)/2)
        if indice > mitad:
            vector.reverse()
            return vector
        else:
            return vector
    except ValueError:
        return vector


def identificarNumeros(vectorRuta):
    #metodo para identificar numeros eb la ruta de cadenas
    for i in range(0, len(vectorRuta)):
        if vectorRuta[i].isdigit():
            vectorRuta[i]=int(vectorRuta[i])    
    return vectorRuta

def armarRuta(ruta):
    ###### LIMPIANDO EL VECTOR DE PUNTOS Y/O RUTAS, PARA OBTENER SOLO PUNTOS O RUTAS VALIDAS#######
    rutax=[] #CREAR UN RUTA VACIAS
    for punto in ruta:
        objRuta=Ruta_flp.objects.filter(nombre_ruta=punto)
        if objRuta.exists() and (not objRuta[0] in rutax):
            rutax.append(objRuta[0])
    return rutax
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


def view_aprobar_flp(request, id_plancompleto):
    if request.user.is_authenticated and request.user.is_active:        
        #var_id = int(id_plancompleto)
        #plan_completo = Flp_trafico.objects.raw("SELECT * FROM plan_vuelo_flp_trafico WHERE id=2728649")#%s",[var_id])[0]
        plan_completo = Flp_trafico.objects.filter(id=id_plancompleto)[0]
        aero='str(plan_completo.id_plan)'
        origen='str(plan_completo.origen)'

        #obteniendo el cuerpo del plan de vuelo tipoavion, velocidad, nivel
        plan_vuelo=str(plan_completo.transponder+plan_completo.texto).split('-')

        cadena=str(plan_completo.transponder+plan_completo.texto)
        
        matricula=''
        try:
            indice=cadena.index('REG/')+4
            for x in range(indice, len(cadena)):
                if cadena[x]!=' ':
                    matricula+=cadena[x]
                else:
                    break
        except ValueError:
            matricula='NFound'

        transmision=''
        try:
            indice=cadena.index('SEL/')+4
            for x in range(indice, len(cadena)):
                if cadena[x]!=' ':
                    transmision+=cadena[x]
                else:
                    break
        except ValueError:
            transmision='NFound'
        velocidad,nivel=plan_vuelo[3][0:9].split('F')
        ficha={'avion':plan_vuelo[1], 'velocidad':  plan_vuelo[3][0:5], 'nivel': plan_vuelo[3][6:9],'salida': plan_vuelo[4][4:9], 'origen': plan_completo.origen[1:5], 'destino': plan_vuelo[4][0:4], 'matricula':matricula, 'transmision':transmision }
        ficha={'avion':plan_vuelo[1], 'velocidad':  plan_vuelo[3][0:5], 'nivel': plan_vuelo[3][6:9],'salida': plan_vuelo[4][4:9], 'origen': plan_completo.origen[1:5], 'destino': plan_vuelo[4][0:4], 'matricula':matricula, 'transmision':transmision }
        #nivel,velocidad=plan_vuelo[3][0:9].split('F')
        #ficha={'avion':plan_vuelo[1], 'velocidad': velocidad, 'nivel': nivel, 'salida': plan_vuelo[4][4:9], 'origen': plan_completo.origen[1:5], 'destino': plan_vuelo[4][0:4] }

        ruta=plan_vuelo[3].split(' ') #RUTA DEL AVION 
        ruta.pop()
        ruta.pop(0)

        ruta=armarRuta(ruta)

        todaruta=Ruta_flp.objects.all()
        todopuntos=EntrePuntos_flp.objects.all()


        context={
            'aero': plan_completo.id_plan, #id_plan            , nombre de la aerolinea
            'plan': str(plan_completo.transponder+'<br>'+plan_completo.texto), #Cuerpo del plan de vuelo
            'ficha': ficha,  #envio de diccionario que contiene tipoavion velocidad niveldevuelo salidaaeropuerto
            'ruta': ruta,
            'todaruta': todaruta,
            'todopuntos': todopuntos
        }
        
        #return render_to_response('temp_plan_vuelo/aprobar_plan.html', context)
        return render(request, 'temp_plan_vuelo/aprobar_plan.html', context ) #retorno el modal y el contexto
    else:
        return redirect('accounts/login/')
    











##VER TABLERO DESLIZABLE EN REACT JS

def view_tablero (request):
    return render(request, 'temp_plan_vuelo/tablero_trello.html')
