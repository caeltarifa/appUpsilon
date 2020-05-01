from django.conf.urls import url, include
from django.urls import path

from apps.plan_vuelo.views import view_plan_vuelo, view_admin, view_aprobar_flp, view_tablero # view_form_plan_vuelo, post_new, post_detail

urlpatterns = [
    url('planvuelo$',view_plan_vuelo, name='index_plan'),
    # url(r'^nuevo$',view_form_plan_vuelo, name='form_plan_vuelo'),
    # url(r'^postnew/', post_new, name='post_new'),
    # url(r'^postdetail/<int:pk>/', post_detail , name='post_detail'),
    url('admin/',view_admin, name='view_admin'), #ver pagina de administrador controlador
    #path('admin_popup/<int:id_plancompleto>/',view_aprobar_flp, name='view_aprobar_flp'),
    path('admin_popup/<int:id_plancompleto>/',view_aprobar_flp, name='view_aprobar_flp'),
    url('tablero/',view_tablero, name='view_tablero'), #ver pagina de administrador controlador
    #path('^admin_popup/(?P<int:id_plancompleto>)/$',view_aprobar_flp, name='view_aprobar_flp'),
    #url(r'^admin_popup/(?P<id_plancompleto>.+)/?$',view_aprobar_flp, name='view_aprobar_flp'),
    
    #path('generacion_fpl/', include('apps.generacion_fpl.urls')),
]