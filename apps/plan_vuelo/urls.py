from django.conf.urls import url, include
from django.urls import path, re_path
from apps.plan_vuelo.views import view_plan_vuelo, view_panel_coordinacion, view_admin_coordinacion , view_aprobar_flp, view_tablero, view_update_flp, view_template_prueba, view_identificacion, view_validar_passwd, view_cerrar_sesion , view_recordar_ruta, view_rutas_guardadas, view_get_trabajadores

from apps.plan_vuelo.views import view_update_notam_realtime,view_notam_modal


from apps.plan_vuelo.views import view_getmetar

from apps.plan_vuelo.views import view_restaurar_ruta, view_archivar_ruta

from apps.plan_vuelo.views import view_guardar_aprobacion, view_historial_aprobacion
# EJECUTIVO ################################################################################################################
from apps.plan_vuelo.views import view_panel_ejecutivo, view_carta_navegacional, view_obtener_dibujo_ruta,view_ver_fpl_aprobado, view_guardar_estado_progreso, view_obtener_fplpanelprogreso


# SUPERVISOR ################################################################################################################
from apps.plan_vuelo.views import view_panel_supervisor, view_servicio_met, view_aeropuertos_aeronaves,view_enviar_fplaeropuerto


 # view_form_plan_vuelo, post_new, post_detail

urlpatterns = [
    path('planvuelo/',view_plan_vuelo, name='index_plan'),
    # url(r'^nuevo$',view_form_plan_vuelo, name='form_plan_vuelo'),
    # url(r'^postnew/', post_new, name='post_new'),
    # url(r'^postdetail/<int:pk>/', post_detail , name='post_detail'),
    path('coordinacion/', view_panel_coordinacion, name="view_panel_coordinacion"), #redirije al panel de control de coordinacion

    path('progreso_vuelos/',view_admin_coordinacion, name='view_admin_coordinacion'), #ver pagina de administrador controlador
    path('admin/update_flp/',view_update_flp, name='view_update_flp'),
    
    #path('admin_popup/<int:id_plancompleto>/',view_aprobar_flp, name='view_aprobar_flp'),
    path('admin_popup/<path:id_plancompleto>/',view_aprobar_flp, name='view_aprobar_flp'),

   ############################################################################# 
    path('identificacion/<int:id_trabajador>/', view_identificacion, name="view_identificacion"),
    path('identificacion/validar/', view_validar_passwd, name="view_validar_passwd"),
    path('identificacion/terminaractividad/', view_cerrar_sesion, name="view_cerrar_sesion"),
    path('identificacion/trabajadores', view_get_trabajadores, name="view_get_trabajadores"),
    

    path('adminy/template_prueba/',view_template_prueba, name='view_template_prueba'),

    url('tablero/',view_tablero, name='view_tablero'), #ver pagina de administrador controlador
    #path('^admin_popup/(?P<int:id_plancompleto>)/$',view_aprobar_flp, name='view_aprobar_flp'),
    #url(r'^admin_popup/(?P<id_plancompleto>.+)/?$',view_aprobar_flp, name='view_aprobar_flp'),
    
    #path('generacion_fpl/', include('apps.generacion_fpl.urls')),

    #gestion de rutas
    path('rutasguardadas/', view_rutas_guardadas, name="view_rutas_guardadas"),
    path('rutasguardadas/restaurar', view_restaurar_ruta, name='view_restaurar_ruta'),
    path('rutasguardadas/archivar', view_archivar_ruta, name='view_archivar_ruta'),
    path('recordarruta/', view_recordar_ruta, name='view_recordar_ruta'),

    #aprobacion de plan de vuelo
    path('aprobarfpl/', view_guardar_aprobacion, name="view_guardar_aprobacion"),
    path('historialaprobados/', view_historial_aprobacion, name="view_historial_aprobacion"),
    
    # EJECUTIVO ################################################################################################################
    path('ejecutivo/', view_panel_ejecutivo, name="view_panel_ejecutivo"), #redirije al panel de control de ejecutivo
    path('cartanavegacional/', view_carta_navegacional, name="view_carta_navegacional"), #
    path('aip/dibujoruta', view_obtener_dibujo_ruta, name="view_obtener_dibujo_ruta"), #
    path('verfplaprobado/<path:id_plancompleto>/',view_ver_fpl_aprobado, name='view_ver_fpl_aprobado'),
    path('guardarestadoprogreso/',view_guardar_estado_progreso, name='view_guardar_estado_progreso'),
    path('getportrabajar/',view_obtener_fplpanelprogreso, name='view_obtener_fplpanelprogreso'),
    


    # SUPERVISOR ################################################################################################################
    path('supervisor/', view_panel_supervisor, name="view_panel_supervisor"), #redirije al panel de control de supervisor
    path('servicio_met/', view_servicio_met, name="view_servicio_met"), #
    path('espacioaereo/', view_aeropuertos_aeronaves, name="view_aeropuertos_aeronaves"), #
    path('getflps/', view_enviar_fplaeropuerto, name="view_enviar_fplaeropuerto"), #
    


    ######################### NOTAMS REAL TIME
    path('notamsupdate/', view_update_notam_realtime, name="view_update_notam_realtime"), #
    path('notammodal/<path:id_notam_mensaje>/',view_notam_modal, name='view_notam_modal'),

    ######################### QUERY METARS
    path('getmetar/<path:id_aeropuerto>/',view_getmetar, name='view_getmetar'),
]