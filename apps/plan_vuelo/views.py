from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.db import connection

#from apps.plan_vuelo.forms import Vuelo_Aprobado_form, PostForm
from apps.plan_vuelo.models import Flp_trafico, Metar_trafico
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
    if request.user.is_authenticated:
        #post=Flp_trafico.objects.raw("select * from plan_vuelo_Flp_trafico where CAST(fecha_llegada AS date) = CAST('2019-10-11' AS date)");
        post=Flp_trafico.objects.raw("select * from plan_vuelo_flp_trafico where hora_amhs like '12%%%%' order by id_amhs desc ")

        metar=Metar_trafico.objects.raw("select * from plan_vuelo_metar_trafico where hora_amhs like '12%%%%' order by id_amhs desc")
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
