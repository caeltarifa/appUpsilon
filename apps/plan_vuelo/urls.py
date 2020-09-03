from django.conf.urls import url, include
from django.urls import path, re_path
from apps.plan_vuelo.views import view_plan_vuelo, view_panel_coordinacion, view_admin_coordinacion , view_aprobar_flp, view_tablero, view_update_flp, view_template_prueba, view_identificacion, view_validar_passwd, view_cerrar_sesion # view_form_plan_vuelo, post_new, post_detail

urlpatterns = [
    path('planvuelo/',view_plan_vuelo, name='index_plan'),
    # url(r'^nuevo$',view_form_plan_vuelo, name='form_plan_vuelo'),
    # url(r'^postnew/', post_new, name='post_new'),
    # url(r'^postdetail/<int:pk>/', post_detail , name='post_detail'),
    path('coordinacion/', view_panel_coordinacion, name="view_panel_coordinacion"), #redirije al panel de control de coordinacion

    path('admin_coordinacion/',view_admin_coordinacion, name='view_admin_coordinacion'), #ver pagina de administrador controlador
    path('admin/update_flp/',view_update_flp, name='view_update_flp'),
    
    #path('admin_popup/<int:id_plancompleto>/',view_aprobar_flp, name='view_aprobar_flp'),
    path('admin_popup/<path:id_plancompleto>/',view_aprobar_flp, name='view_aprobar_flp'),
    
    path('identificacion/<int:id_trabajador>/', view_identificacion, name="view_identificacion"),
    path('identificacion/validar', view_validar_passwd, name="view_validar_passwd"),

    path('identificacion/terminaractividad', view_cerrar_sesion, name="view_cerrar_sesion"),
    

    path('adminy/template_prueba/',view_template_prueba, name='view_template_prueba'),

    url('tablero/',view_tablero, name='view_tablero'), #ver pagina de administrador controlador
    #path('^admin_popup/(?P<int:id_plancompleto>)/$',view_aprobar_flp, name='view_aprobar_flp'),
    #url(r'^admin_popup/(?P<id_plancompleto>.+)/?$',view_aprobar_flp, name='view_aprobar_flp'),
    
    #path('generacion_fpl/', include('apps.generacion_fpl.urls')),
]