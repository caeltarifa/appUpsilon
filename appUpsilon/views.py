from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse

#from apps.plan_vuelo.forms import Vuelo_Aprobado_form, PostForm
from apps.plan_vuelo.models import Flp_trafico

# Create your views here.

def view_pagina_principal(request):
    if request.user.is_authenticated:
        return redirect('view_admin')
    else:
        return redirect('accounts/login/')

    #return render(request, 'temp_plan_vuelo/index.html')
