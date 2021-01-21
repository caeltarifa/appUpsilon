from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse

from django.contrib.auth.models import Group

#from apps.plan_vuelo.forms import Vuelo_Aprobado_form, PostForm
from apps.plan_vuelo.models import Flp_trafico

# Create your views here.

def view_pagina_principal(request):
    
    #### IMPORTANTE --- :user: adminupsilon pertenece a todos los grupos
    
    if request.user.is_authenticated: 
        #preguntando si el 'usuario autenticado' pertenece al grupo de CONTROLADORES
        #if request.user.groups.filter(name='AROAISLP').exists():
        #    if request.user.username in 'aroaislp@aasana':
        #        return redirect('view_admin_ais')
        
        #preguntando si el 'usuario autenticado' pertenece al grupo de aerolineas
        if request.user.groups.filter(name='EMPRESASLP').exists():
            if request.user.username in 'AMASZONAS':
                return redirect('view_admin_amaszonas')
            
            if request.user.username in 'ECOJET':
                return redirect('view_admin_ecojet')
            
            if request.user.username in 'aviancalp@aasana':
                return redirect('view_admin_avianca')
        
        #preguntando si el 'usuario autenticado' pertenece al grupo de FELCN
        if request.user.groups.filter(name='FELCN').exists():
            if request.user.username in 'felcnlp@aasana':
                return redirect('view_admin_felcn')
        
        #preguntando si el 'usuario autenticado' pertenece al grupo de COMUNICACIONES
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
                
            

        #RETURN POR DEFECTO
        return render(request, 'temp_plan_vuelo/prohibido.html' )#,'metar':metar} )

    else:
        return redirect('accounts/login/')


def view_panel_comunicaciones(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='COMUNICACIONESLP').exists():
        return render(request, 'temp_plan_vuelo/index_comunicacion.html')# ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
    else:
        return redirect('login')


def view_admin_comunicaciones(request):
    #def view_panel_coordinacion(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='COMUNICACIONESLP').exists():
        return render(request, 'temp_plan_vuelo/index_coordinacion.html')# ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
    else:
        return redirect('login')






# def control_acceso_login(request):
#     if request.user.is_authenticated or request.user.is_active:
#         view_pagina_principal(request)
#     else:
#         return render(request, 'registration/already_logged.html')
        #return redirect('accounts/login/') 