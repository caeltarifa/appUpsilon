from django.conf.urls import url, include
from django.urls import path, re_path

# ARO AIS ################################################################################################################
from apps.aro_ais.views import view_admin_ais, view_panel_aroaislp, view_panel_notaminternacional
from apps.aro_ais.views import view_pib_automatizado, view_archivar_pib, view_publicarguardar_pib, view_pib_tiemporeal,view_pibupdate_tiemporeal
from apps.aro_ais.views import view_guardarregistro_pib
from apps.aro_ais.views import view_imprimir_pibrealtime
from apps.aro_ais.views import view_panel_serviciosaroais_aasana
from apps.aro_ais.views import view_new_notam
from apps.aro_ais.views import view_replace_notam
from apps.aro_ais.views import view_cancel_notam
from apps.aro_ais.views import view_getAsunto,view_getEstadoAsunto
from apps.aro_ais.views import view_codigos_abreviaturas
from apps.aro_ais.views import view_get_abreviatura8400
from apps.aro_ais.views import view_get_codigo8126


urlpatterns = [
    path('',view_panel_aroaislp, name="view_panel_aroaislp"),
    
    path('nof',view_panel_notaminternacional, name="view_panel_notaminternacional"),
    path('asunto8126',view_getAsunto, name="view_getAsunto"),
    path('estado_asunto8126',view_getEstadoAsunto, name="view_getEstadoAsunto"),

    path('slcb/', view_panel_serviciosaroais_aasana, name="view_panel_aisslcb"),
    path('slvr/', view_panel_serviciosaroais_aasana, name="view_panel_aisslvr"),
    path('sltr/', view_panel_serviciosaroais_aasana, name="view_panel_aissltr"),
    
    path('aroaisfpl/',view_admin_ais, name='view_admin_ais'),
    
    path('pibautomatizado/', view_pib_automatizado, name="view_pib_automatizado"), #
    path('archivarpib/', view_archivar_pib, name="view_archivar_pib"), #archiva pib
    path('publicarguardar/', view_publicarguardar_pib, name="view_publicarguardar_pib"), #archiva pib
    path('pibtiemporeal/', view_pib_tiemporeal, name="view_pib_tiemporeal"), #archiva pib
    path('verpib/', view_pibupdate_tiemporeal, name="view_pibupdate_tiemporeal"), #envia al frontend datos actualizados
    path('guardarregistropib/', view_guardarregistro_pib, name="view_guardarregistro_pib"), #envia al frontend datos actualizados
    path('imprimirpib/', view_imprimir_pibrealtime, name="view_imprimir_pibrealtime"), #INTERFAZ PARA IMPRIMIR EL PIB
    path('newnotam/', view_new_notam, name="view_new_notam"), #SIMULADOR GENERADOR DE NOTAM
    path('replacenotam/', view_replace_notam, name="view_replace_notam"), #SIMULADOR GENERADOR DE NOTAM
    path('cancelnotam/', view_cancel_notam, name="view_cancel_notam"), #SIMULADOR GENERADOR DE NOTAM
    path('codigos_abreviaturas/', view_codigos_abreviaturas, name="view_codigos_abreviaturas"), #SIMULADOR GENERADOR DE NOTAM


    ## CODIGOS Y ABREVIATURAS
    path('responseabreviatura/', view_get_abreviatura8400, name="view_get_abreviatura8400"), #
    path('response8126/', view_get_codigo8126, name="view_get_codigo8126"), #
]