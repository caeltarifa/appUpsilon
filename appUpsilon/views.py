from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse

from django.contrib.auth.models import Group

#from apps.plan_vuelo.forms import Vuelo_Aprobado_form, PostForm
from apps.plan_vuelo.models import Flp_trafico

# Create your views here.

def view_pagina_principal(request):
    #asd
    if request.user.is_authenticated: 
        #preguntando si pertenece al grupo de CONTROLADORES
        if request.user.groups.filter(name='CONTROLADORES').exists():
            if request.user.username in 'aroaislp@aasana':
                return redirect('view_admin_ais')
        
        #preguntando si pertenece al grupo de aerolineas
        if request.user.groups.filter(name='AEROLINEA').exists():
            if request.user.username in 'AMASZONAS':
                return redirect('view_admin_amaszonas')
            if request.user.username in 'ECOJET':
                return redirect('view_admin_ecojet')
            if request.user.username in 'AVIANCA':
                return redirect('view_admin_avianca')
        
        #preguntando si pertenece al grupo de FELCN
        if request.user.groups.filter(name='FELCN').exists():
            return redirect('view_admin_felcn')
        
        #preguntando si pertenece al grupo de COMUNICACIONES
        if request.user.groups.filter(name='COMUNICACIONES').exists():
            if request.user.username in 'ccamlp@aasana':
                return redirect('view_admin_comunicaciones')

        #RETURN POR DEFECTO
        return redirect('view_admin')
    else:
        return redirect('accounts/login/')

    #return render(request, 'temp_plan_vuelo/index.html')

# def control_acceso_login(request):
#     if request.user.is_authenticated or request.user.is_active:
#         view_pagina_principal(request)
#     else:
#         return render(request, 'registration/already_logged.html')
        #return redirect('accounts/login/') 