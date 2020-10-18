from django.conf.urls import url, include
from django.urls import path

from apps.generacion_fpl.views import  view_admin_felcn, view_admin_empresa,  view_save_fpl


#VISTAS PARA USUARIOS EMPRESA
from apps.generacion_fpl.views import  view_solicitar_comunicacional, view_solicitar_operacional,view_solicitar_suplementaria, view_creacion_fpl_presentado, view_solicitar_felcn, view_cancelar_fpl,view_mostrar_fpl_empresa

#VISTAS PARA USUARIOS FELCN
from apps.generacion_fpl.views import view_aprobar_codigo_felcn

#VISTAS PARA USUARIOS ARO AIS

#VISTA SOLICITUD DE CODIGO DE APROBACION
from apps.generacion_fpl.views import view_codigo_solicitud, view_aprobar_codigo

urlpatterns = [
    #url('^$',view_index_generacion, name='view_index_generacion'),
    url('^felcn$',view_admin_felcn, name='view_admin_felcn'),
    
    # urls para las empresas
    url('^amaszonaslp$',view_admin_empresa, name='view_admin_amaszonas'),
    url('^aviancalp$',view_admin_empresa, name='view_admin_avianca'),
    url('^ecojetlp$',view_admin_empresa, name='view_admin_ecojet'),
    # urls para las empresas
    


    #url('^comunicaciones$',view_admin_comunicaciones, name='view_admin_comunicaciones'),
    
    
    url('^crear_fpl$',view_creacion_fpl_presentado, name='view_creacion_fpl_presentado'),
    url('^solicitar_fplcom$',view_solicitar_comunicacional, name='view_solicitar_comunicacional'),
    url('^solicitar_fplope$',view_solicitar_operacional, name='view_solicitar_operacional'),
    url('^solicitar_fplsup$',view_solicitar_suplementaria, name='view_solicitar_suplementaria'),
    url('^solicitar_felcn$',view_solicitar_felcn, name='view_solicitar_felcn'),
    url('^cancelar_fpl$',view_cancelar_fpl, name='view_cancelar_fpl'),
    url('^mostrar_fpl$',view_mostrar_fpl_empresa, name='view_mostrar_fpl_empresa'),
    url('^aprobacion$',view_codigo_solicitud, name='view_codigo_solicitud'),
     
    #url para aprobar con codigo de despachador de vuelo.
    url('^aprobacioncodigo$',view_aprobar_codigo, name='view_aprobar_codigo'),
    
    #url para aprobar con codigo de despachador de vuelo.
    url('^aprobacioncodigofelcn$',view_aprobar_codigo_felcn, name='view_aprobar_codigo_felcn'),

    #url('^solicitar_fplsup/<int:id_fpl_presentado>/',view_solicitar_suplementaria, name='view_solicitar_suplementaria'),
    path('save_popup/<plan_solicitado>/',view_save_fpl, name='view_save_fpl'),




    #path('plan_vuelo/', include('apps.plan_vuelo.urls')),
]