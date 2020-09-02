from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.db import connection

from datetime import datetime
import time

from django.db.models import Q
#from django.shortcuts import render_to_response



############# LIBRERIA PARA AUTENTICAR USUARIOS ##############
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
##############################################################






# Create your views here.

from apps.plan_vuelo.models import Flp_trafico, EntrePuntos_flp,Ruta_flp, Empresa_institucion, Trabajador
from apps.generacion_fpl.models import Comunicacional, Operacional, Suplementaria, Plan_vuelo_presentado
from apps.generacion_fpl.form_com import ComunicacionalForm, OperacionalForm, SuplementariaForm, Plan_presentadoForm

#importando el modelo para acceder a datos de recursos humanos RRHH
from apps.trabajadoresATS.models import TrabajadoresATS, CuentasATS

# Create your views here.

def view_admin_ais(request):
    if request.user.is_authenticated:
        trabajadores= TrabajadoresATS.objects.using('aasana_bd').raw("select * from trabajadores limit 5 ")

        cuentas= CuentasATS.objects.using('aasana_bd').raw("select * from cuentas limit 5 ")

        respuesta= CuentasATS.objects.using('aasana_bd').raw("select id_cuenta, password, usuario from cuentas where id_cuenta=1 ")[0]
        
        respuesta=respuesta.usuario + '----'+ respuesta.password


        return render(request, 'temp_plan_vuelo/aroais.html', {'trabajadores':trabajadores, 'cuentas':cuentas, 'respuesta':respuesta} )
    else:
        return redirect('login')



def view_admin_felcn(request):
    if request.user.is_authenticated:
        
        usuariox=str(request.user.username).split('@')
        
        #preguntando si el nombre_usuario es igual a algun nombre empresa_institucion y obteniendo su id_empresa
        
        #preguntando si es usuario rutorizado
        if not Empresa_institucion.objects.filter(nombre_emp_inst=usuariox[0]).exists():
            return render(request, 'temp_plan_vuelo/no_autorizado.html')

        id_empresa=Empresa_institucion.objects.filter(nombre_emp_inst=usuariox[0])[0].id_emp_inst
        trabajadores=Trabajador.objects.values('ci', 'nombre', 'apellido').filter(empresa_institucion_id=int(id_empresa))
        
        #OBTENIENDO PLANES DE VUELOS CREADOS, SOLICITADOS Y CANCELADOS
        solicitados=Plan_vuelo_presentado.objects.raw('select distinct id_fpl_presentado, nro_formulario, fecha_presentacion, hora_presentacion, parte_operacional_id,parte_suplementaria_id ,plan_vuelo_trabajador.nombre, plan_vuelo_trabajador.apellido, plan_vuelo_empresa_institucion.nombre_emp_inst, generacion_fpl_estado.nombre_estado,generacion_fpl_plan_vuelo_presentado.fk_estado_id from generacion_fpl_plan_vuelo_presentado INNER JOIN plan_vuelo_trabajador ON plan_vuelo_trabajador.ci=generacion_fpl_plan_vuelo_presentado.fk_despachador_id INNER JOIN plan_vuelo_empresa_institucion ON plan_vuelo_empresa_institucion.id_emp_inst=plan_vuelo_trabajador.empresa_institucion_id INNER JOIN generacion_fpl_estado ON generacion_fpl_estado.id_estado=generacion_fpl_plan_vuelo_presentado.fk_estado_id where (generacion_fpl_plan_vuelo_presentado.fk_estado_id=1)')
        # id_fpl_presentado | nro_formulario | fecha_presentacion | hora_presentacion | parte_operacional_id | parte_suplementaria_id | nombre | apellido | nombre_emp_inst | nombre_estado | fk_estado_id  
        
        return render(request, 'temp_plan_vuelo/felcn.html', {'solicitados':solicitados, 'id_empresa':id_empresa, 'trabajadores':trabajadores})
    else:
        return redirect('logout')



def view_admin_empresa(request):
    if request.user.is_authenticated:
        usuariox=str(request.user.username).split('@')
        
        #preguntando si existe el usuario en la tabla 'Empresa_institucion'
        if not Empresa_institucion.objects.filter(nombre_emp_inst=usuariox[0]).exists():
            return render(request, 'temp_plan_vuelo/no_autorizado.html')

        id_empresa=Empresa_institucion.objects.filter(nombre_emp_inst=usuariox[0])[0].id_emp_inst
        trabajadores=Trabajador.objects.values('ci', 'nombre','apellido').filter(empresa_institucion_id=int(id_empresa))
        
        #OBTENIENDO PLANES DE VUELOS CREADOS, SOLICITADOS Y CANCELADOS
        solicitados=Plan_vuelo_presentado.objects.raw('select distinct id_fpl_presentado, nro_formulario, fecha_presentacion, hora_presentacion, parte_operacional_id,parte_suplementaria_id ,plan_vuelo_trabajador.nombre, plan_vuelo_trabajador.apellido, plan_vuelo_empresa_institucion.nombre_emp_inst, generacion_fpl_estado.nombre_estado,generacion_fpl_plan_vuelo_presentado.fk_estado_id from generacion_fpl_plan_vuelo_presentado INNER JOIN plan_vuelo_trabajador ON plan_vuelo_trabajador.ci=generacion_fpl_plan_vuelo_presentado.fk_despachador_id INNER JOIN plan_vuelo_empresa_institucion ON plan_vuelo_empresa_institucion.id_emp_inst=plan_vuelo_trabajador.empresa_institucion_id INNER JOIN generacion_fpl_estado ON generacion_fpl_estado.id_estado=generacion_fpl_plan_vuelo_presentado.fk_estado_id     where plan_vuelo_empresa_institucion.id_emp_inst='+str(id_empresa)+ 'and (generacion_fpl_plan_vuelo_presentado.fk_estado_id<4 or generacion_fpl_plan_vuelo_presentado.fk_estado_id=7) order by nro_formulario desc')
        # id_fpl_presentado | nro_formulario | fecha_presentacion | hora_presentacion | parte_operacional_id | parte_suplementaria_id | nombre | apellido | nombre_emp_inst | nombre_estado | fk_estado_id  
        
        #OBTENIENDO PLANES DE VUELOS APROBADOS POR ARO-AIS
        aprobados=Plan_vuelo_presentado.objects.raw('select id_fpl_presentado, nro_formulario, fecha_presentacion, hora_presentacion,plan_vuelo_trabajador.nombre, plan_vuelo_trabajador.apellido ,date_estado_ais,id_aeronave,aerodromo_salida, hora_salida, aerodromo_destino,fk_estado_id from generacion_fpl_plan_vuelo_presentado INNER JOIN generacion_fpl_operacional ON generacion_fpl_plan_vuelo_presentado.parte_operacional_id=generacion_fpl_operacional.id_operacional INNER JOIN plan_vuelo_trabajador on plan_vuelo_trabajador.ci = generacion_fpl_plan_vuelo_presentado.fk_despachador_id where fk_estado_id=5 and plan_vuelo_trabajador.empresa_institucion_id='+str(id_empresa))
        #id_fpl_presentado | nro_formulario | fecha_presentacion | hora_presentacion | nombre | apellido | date_estado_ais | id_aeronave | aerodromo_salida | hora_salida | aerodromo_destino | fk_estado_id 
        #aprobados=Plan_vuelo_presentado.objects.raw('select * from generacion_fpl_plan_vuelo_presentado where fk_despachador_id in (select ci from plan_vuelo_trabajador where fk_despachador_id=ci and empresa_institucion_id='+str(id_empresa)+' and fk_estado_id=5);')
        
        #OBTENIENDO PLANES DE VUELOS RECHAZADOS FELCN O RECHAZADOS ARO-AIS
        rechazados=Plan_vuelo_presentado.objects.raw('select id_fpl_presentado, nro_formulario, fecha_presentacion, hora_presentacion, nombre,apellido,nombre_estado, arg_rechazo_policia, arg_rechazo_ais, date_estado_ais, date_estado_policia, id_aeronave, aerodromo_salida, hora_salida, aerodromo_destino from generacion_fpl_plan_vuelo_presentado INNER JOIN generacion_fpl_operacional ON generacion_fpl_operacional.id_operacional=parte_operacional_id INNER JOIN generacion_fpl_estado ON generacion_fpl_estado.id_estado=fk_estado_id INNER JOIN plan_vuelo_trabajador ON plan_vuelo_trabajador.ci=fk_despachador_id where (fk_estado_id=4 or fk_estado_id=6) and plan_vuelo_trabajador.empresa_institucion_id='+str(id_empresa))
        #id_fpl_presentado | nro_formulario | fecha_presentacion | hora_presentacion |  nombre_estado  | arg_rechazo_policia | arg_rechazo_ais | date_estado_ais | date_estado_policia | id_aeronave | aerodromo_salida | hora_salida | aerodromo_destino
        #rechazados=Plan_vuelo_presentado.objects.raw('select * from generacion_fpl_plan_vuelo_presentado where fk_despachador_id in (select ci from plan_vuelo_trabajador where fk_despachador_id=ci and empresa_institucion_id='+str(id_empresa)+' and (fk_estado_id=6 or fk_estado_id=4));')

        #OBTENIENDO EL METAR 
        #---metar=Metar_trafico.objects.raw("select * from plan_vuelo_metar_trafico order by fecha_llegada desc limit 50")


        return render(request, 'temp_plan_vuelo/adminempresa.html', {'id_empresa':id_empresa, 'solicitados':solicitados,'rechazados':rechazados , 'aprobados':aprobados, 'metar':metar, 'trabajadores':trabajadores} )
    else:
        return redirect('login')

def view_admin_comunicaciones(request):
    if request.user.is_authenticated:
        
        usuariox=str(request.user.username).split('@')
        #preguntando si el nombre_usuario es igual a algun nombre empresa_institucion y obteniendo su id_empresa
        #id_empresa=Empresa_institucion.objects.filter(nombre_emp_inst=usuariox[0])[0].id_emp_inst

        return render(request, 'temp_plan_vuelo/comunicaciones.html', {'id_empresa':usuariox[0]} )
    else:
        return redirect('login')


##SOLICITUDES DE CREACION DE PLAN_PRESENTADO
def view_creacion_fpl_presentado(request):
    if request.user.is_authenticated:
        
        usuariox=str(request.user.username).split('@')

        id_empresa=Empresa_institucion.objects.filter(nombre_emp_inst=usuariox[0])[0].id_emp_inst
        trabajadores=Trabajador.objects.values('ci', 'nombre','apellido').filter(empresa_institucion_id=int(id_empresa))
        
        if request.method == 'POST':
            form_fpl=Plan_presentadoForm(request.POST)
            if form_fpl.is_valid():
                form_fpl.save()
            return redirect('/')
        else:
            form_fpl=Plan_presentadoForm()
            numeroform=Plan_vuelo_presentado.objects.all().count()+1
            
            hora=str(datetime.now().hour)+':'+str(datetime.now().minute)+':'+str(datetime.now().second)
            hoy=str(datetime.now().year)+'-'+str(datetime.now().month)+'-'+str(datetime.now().day)
            return render(request, 'temp_plan_vuelo/modal_crear_flp.html', {'form_fpl':form_fpl,'numeroform':numeroform, 'hoy':hoy, 'hora':hora, 'trabajadores': trabajadores })

## DEVUELVE EL MODAL PARA VALIDAR CODIGO 
def view_codigo_solicitud(request):
    if request.user.is_authenticated:
        #captura id de la empresa
        id_empresa=Empresa_institucion.objects.filter(nombre_emp_inst=request.user.username)[0].id_emp_inst
        
        #captura el id_plan_vuelo_presentado
        id_presentado=request.GET.get('idpresentado',False)
        
        #lista de trabajadores de la cuenta de usuario
        trabajadores=Trabajador.objects.values('ci', 'nombre','apellido').filter(empresa_institucion_id=int(id_empresa))
        
        #quien=Plan_vuelo_presentado.objects.raw('select nro_formulario, fecha_presentacion, hora_presentacion, generacion_fpl_operacional.id_aeronave from generacion_fpl_plan_vuelo_presentado inner join generacion_fpl_operacional on generacion_fpl_plan_vuelo_presentado.parte_operacional_id=generacion_fpl_operacional.id_operacional where generacion_fpl_plan_vuelo_presentado.id_fpl_presentado=9')
        quien=Plan_vuelo_presentado.objects.filter(id_fpl_presentado=int(id_presentado)).values('fecha_presentacion','hora_presentacion', 'parte_operacional_id')[0]
        aeronave=Operacional.objects.filter(id_operacional=int(quien['parte_operacional_id'])).values('id_aeronave')[0]
        #enviar
        #Nro formulario, fecha presentacion, nombre trabajador, ci ,BOV123
        return render(request, 'temp_plan_vuelo/modal_codigo_solicitud.html', {'quien':quien, 'aeronave':aeronave,'trabajadores': trabajadores ,'id_presentado':id_presentado})
    else:
        return redirect('login') #redireccionar al forbiden

## VALIDANDO EL CODIGO DE APROBACION PARA SOLICITAR A LA FELCN
def view_aprobar_codigo(request):
    if request.user.is_authenticated:
        #quien_eres='select id_fpl_presentado, nro_formulario, fecha_presentacion, hora_presentacion, id_aeronave, nombre, apellido, ci from generacion_fpl_plan_vuelo_presentado inner join generacion_fpl_operacional on generacion_fpl_plan_vuelo_presentado.parte_operacional_id=generacion_fpl_operacional.id_operacional inner join plan_vuelo_trabajador on generacion_fpl_plan_vuelo_presentado.fk_despachador_id=plan_vuelo_trabajador.ci where plan_vuelo_trabajador.empresa_institucion_id=%s' + '4' + 'and generacion_fpl_plan_vuelo_presentado.fk_despachador_id=%s'+'8346123'
        
        #captura id de la empresa
        id_empresa=Empresa_institucion.objects.filter(nombre_emp_inst=request.user.username)[0].id_emp_inst
        
        #captura el codigo
        codigoin=request.GET.get('codigo',False)

        #capturar el ci
        citra=request.GET.get('idtra',False)

        #capturar el id_plan_presentado
        id_presentado=request.GET.get('idpresentado',False)

        #preguntando si el usuario existe
        despachador=Trabajador.objects.filter(empresa_institucion_id=int(id_empresa), ci=citra)
        if despachador.exists():
            if despachador[0].codigo==codigoin:
                Plan_vuelo_presentado.objects.filter(id_fpl_presentado=int(id_presentado)).update(fk_estado_id=1, fk_despachador_id=citra)
        return redirect('/')
        #return render(request, 'temp_plan_vuelo/modal_codigo_solicitud.html', {'quien':quien, 'aeronave':aeronave,'trabajadores': trabajadores })
    else:
        return redirect('login') #redireccionar al forbiden



## VALIDANDO EL CODIGO DE APROBACION DE FPL PARA POLICIAS 
## DEVUELVE EL MODAL PARA VALIDAR CODIGO DE POLICIA 
def view_aprobar_codigo_felcn(request):
    if request.user.is_authenticated:
        #captura id de la empresa
        usuariox=str(request.user.username).split('@')
        id_empresa=Empresa_institucion.objects.filter(nombre_emp_inst=usuariox[0])[0].id_emp_inst
        
        #captura el id_plan_vuelo_presentado
        id_presentado=request.GET.get('idpresentado',False)
        
        #lista de trabajadores de la cuenta de usuario
        trabajadores=Trabajador.objects.values('ci', 'nombre','apellido').filter(empresa_institucion_id=int(id_empresa))
        
        #quien=Plan_vuelo_presentado.objects.raw('select nro_formulario, fecha_presentacion, hora_presentacion, generacion_fpl_operacional.id_aeronave from generacion_fpl_plan_vuelo_presentado inner join generacion_fpl_operacional on generacion_fpl_plan_vuelo_presentado.parte_operacional_id=generacion_fpl_operacional.id_operacional where generacion_fpl_plan_vuelo_presentado.id_fpl_presentado=9')
        quien=Plan_vuelo_presentado.objects.filter(id_fpl_presentado=int(id_presentado)).values('fecha_presentacion','hora_presentacion', 'parte_operacional_id')[0]
        aeronave=Operacional.objects.filter(id_operacional=int(quien['parte_operacional_id'])).values('id_aeronave')[0]
        #enviar
        #Nro formulario, fecha presentacion, nombre trabajador, ci ,BOV123
        return render(request, 'temp_plan_vuelo/modal_codigo_solicitud_felcn.html', {'quien':quien, 'aeronave':aeronave,'trabajadores': trabajadores ,'id_presentado':id_presentado})
    else:
        return redirect('login') #redireccionar al forbiden





##SOLICITUDES DE CREACION DE PLAN COMUNICACIONAL
def view_solicitar_comunicacional(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            formulario=ComunicacionalForm(request.POST)
            if formulario.is_valid():
                formulario.save()
            return redirect('/')
        else:
            formulario=ComunicacionalForm()
            return render(request, 'temp_plan_vuelo/modal_solicitar_flp.html', {'formulario':formulario}  )
    else:
        return redirect('login') #redireccionar al forbiden


##SOLICITUDES DE CREACION DE PLAN OPERACIONAL
def view_solicitar_operacional(request):
    if request.user.is_authenticated:
        id_presentado=request.GET.get('idpresentado',False)
        if request.method =='POST':
            form_operacional=OperacionalForm(request.POST)
            if form_operacional.is_valid:
                oper=form_operacional.save()
                Plan_vuelo_presentado.objects.filter(id_fpl_presentado=int(id_presentado)).update(parte_operacional_id=oper.id_operacional)
            return redirect('/')
        else:
            form_operacional=OperacionalForm()
            return render(request, 'temp_plan_vuelo/modal_solicitar_flp_oper.html', {'form_operacional':form_operacional, 'id_presentado':id_presentado}  )
    else:
        return redirect('login') #redireccionar al forbiden


##SOLICITUDES DE CREACION DE PLAN SUPLEMENTARIA
def view_solicitar_suplementaria(request):
    if request.user.is_authenticated:
        
        id_presentado=request.GET.get('idpresentado',False)
        
        if request.method =='POST':
            form_suplementaria=SuplementariaForm(request.POST)
            if form_suplementaria.is_valid:
                suple=form_suplementaria.save()
                Plan_vuelo_presentado.objects.filter(id_fpl_presentado=int(id_presentado)).update(parte_suplementaria_id=suple.id_suplementaria)
            return redirect('/')
        else:
            form_suplementaria=SuplementariaForm()
            return render(request, 'temp_plan_vuelo/modal_solicitar_flp_suple.html', {'form_suplementaria':form_suplementaria, 'id_presentado':id_presentado} )
    else:
        return redirect('login') #redireccionar al forbiden

def view_save_fpl(request):
    if request.user.is_authenticated:
        return redirect('logout')
    else:
        return redirect('login')

## ENVIAR SOLICITUD A FELCN
def view_solicitar_felcn(request):
    if request.user.is_authenticated:
        id_presentado=request.GET.get('idpresentado',False)
        Plan_vuelo_presentado.objects.filter(id_fpl_presentado=int(id_presentado)).update(fk_estado_id=1)
        return redirect('login')
    else:
        return redirect('logout')


## CANCELAR EL FPL SOLICITADO
def view_cancelar_fpl(request):
    if request.user.is_authenticated:
        id_presentado=request.GET.get('idpresentado',False)
        Plan_vuelo_presentado.objects.filter(id_fpl_presentado=int(id_presentado)).update(fk_estado_id=2)
        
        ## AGREGAR LA HORA QUE SE ESTA CANCELANDO
        #Plan_vuelo_presentado.objects.filter(id_fpl_presentado=int(id_presentado)).update(fk_estado_id=2)

        return redirect('/')
    else:
        return redirect('login')

## VER FPL CREADO EN SU PARTE OPERACIONAL AND SUPLEMENTARIA
def view_mostrar_fpl_empresa(request):
    if request.user.is_authenticated:
        id_presentado=request.GET.get('idpresentado',False)
        
        # OBTENER LA PARTE OPERACIONAL 
        #operacional=Operacional.objects.filter(id_operacional=Plan_vuelo_presentado.objects.filter(id_fpl_presentado=id_presentado).values('parte_operacional_id')[0].get('parte_operacional_id'))[0]
        
        datosCreacion=Plan_vuelo_presentado.objects.filter(id_fpl_presentado=int(id_presentado)).values('nro_formulario','fecha_presentacion', 'hora_presentacion')[0]

        id_ops=Plan_vuelo_presentado.objects.filter(id_fpl_presentado=int(id_presentado))[0].parte_operacional_id
        operacional=Operacional.objects.filter(id_operacional=int(id_ops))[0]
        formoper=OperacionalForm(instance=operacional)
        
        # # OBTENER LA PARTE SUPLEMENTARIA
        suplementaria=Suplementaria.objects.filter(id_suplementaria=Plan_vuelo_presentado.objects.filter(id_fpl_presentado=id_presentado).values('parte_suplementaria_id')[0].get('parte_suplementaria_id'))[0]
        formsuple=SuplementariaForm(instance=suplementaria)

        if request.method == "POST":
            formoper=OperacionalForm(request.POST, instance=operacional)
            # formsuple=SuplementariaForm(request.POST, instance=suplementaria)
            
            if formoper.is_valid():
                operacional=formoper.save(commit=False)
                #operacional.save()
            
            if formsuple.is_valid():
                suplementaria=formsuple.save(commit=False)
                #suplementaria.save()
            
        return render(request, 'temp_plan_vuelo/modal_mostrar_flp_empresa.html', {'form_operacional':formoper, 'form_suplementaria':formsuple, 'datosCreacion':datosCreacion})
    else:
        return redirect('login')

## <VISTAS DE USUARIO EMPRESA >
   
    #PARA MOSTRAR LOS PLANES DE VUELO SOLICITADOS
# def view_mostrar_solicitados(request):
#     if request.user.is_authenticated and request.user.groups.filter(name='EMPRESA').exists():
#         planes_solicitados=Plan_vuelo_presentado.objects



## </VISTAS DE USUARIO EMPRESA >



#         return redirect('login')