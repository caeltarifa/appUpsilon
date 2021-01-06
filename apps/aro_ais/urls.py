from django.conf.urls import url, include
from django.urls import path, re_path

# ARO AIS ################################################################################################################
from apps.aro_ais.views import view_admin_ais, view_panel_aroaislp, view_panel_notaminternacional
from apps.aro_ais.views import view_pib_automatizado, view_archivar_pib, view_publicarguardar_pib, view_pib_tiemporeal,view_pibupdate_tiemporeal
from apps.aro_ais.views import view_guardarregistro_pib
from apps.aro_ais.views import view_imprimir_pibrealtime
from apps.aro_ais.views import view_panel_serviciosaroais_aasana
from apps.aro_ais.views import view_simulador
from apps.aro_ais.views import view_getAsunto,view_getEstadoAsunto
from apps.aro_ais.views import view_diccionario8400

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
    path('simulador/', view_simulador, name="view_simulador"), #SIMULADOR GENERADOR DE NOTAM
    path('diccionario8400/', view_diccionario8400, name="view_diccionario8400"), #SIMULADOR GENERADOR DE NOTAM


]