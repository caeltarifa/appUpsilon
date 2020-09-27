from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.contrib.auth.models import Group
import datetime
import json


# Create your views here.


from apps.plan_vuelo.models import Flp_trafico, EntrePuntos_flp,Ruta_flp, Trabajador, Ruta_guardada, Flp_aprobado, Punto_satelital, Notam_trafico, Aeropuerto


# Create your views here.

def view_panel_aroais(request):
    if request.user.is_authenticated and request.user.is_active  and request.user.groups.filter(name='AROAISLP').exists():
        equipo_coordinacion = Trabajador.objects.raw("select ci, nombre, apellido, activo from plan_vuelo_trabajador where ci in (select ci from plan_vuelo_trabajador_cargo where cargo_id=1 and ci=trabajador_id) and empresa_institucion_id=1 order by activo")
        return render(request, 'temp_plan_vuelo/index_aroais.html' ,{'equipo_trabajo': equipo_coordinacion} )#,'metar':metar} )
    else:
        return redirect('login')
