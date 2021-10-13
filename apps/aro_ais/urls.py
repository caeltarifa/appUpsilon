from django.conf.urls import url, include
from django.urls import path, re_path

# ARO AIS ################################################################################################################
from apps.aro_ais.views import view_admin_ais, view_panel_aroaislp, view_panel_notaminternacional
from apps.aro_ais.views import view_pib_automatizado, view_archivar_pib, view_publicarguardar_pib, view_pib_tiemporeal,view_pibupdate_tiemporeal

from apps.aro_ais.views import view_pib_tiemporeal2

from apps.aro_ais.views import view_guardarregistro_pib
from apps.aro_ais.views import view_imprimir_pibrealtime
from apps.aro_ais.views import view_ais_for_aed

from apps.aro_ais.views import view_new_notam, view_new_notam_2

from apps.aro_ais.views import view_getAsunto,view_getEstadoAsunto
from apps.aro_ais.views import view_codigos_abreviaturas
from apps.aro_ais.views import view_get_abreviatura8400
from apps.aro_ais.views import view_get_codigo8126
from apps.aro_ais.views import view_get_lista_asuntos_8126
from apps.aro_ais.views import view_get_lista_estados_8126

from apps.aro_ais.views import view_get_correlativo_charly
from apps.aro_ais.views import view_get_correlativo_alfa


from appUpsilon.views import api_historico_charly_from_notamn
from appUpsilon.views import api_historico_charly_from_notamr
from appUpsilon.views import api_historico_charly_from_notamc


from appUpsilon.views import api_historico_alfa_from_notamn
from appUpsilon.views import api_historico_alfa_from_notamr
from appUpsilon.views import api_historico_alfa_from_notamc

from apps.aro_ais.views import view_todos_notams
from apps.aro_ais.views import view_banco_notam


from apps.aro_ais.views import view_notam_modal_charly
from apps.aro_ais.views import view_notam_modal_alfa


from apps.aro_ais.views import view_get_aed_georef

##CREAR NOTAM
from apps.aro_ais.views import view_post_crear_notam

from apps.aro_ais.views import view_api_notam_search
from apps.aro_ais.views import view_api_notam_search_string

##recuperar datos del servidor de NOTAM pasado
from apps.aro_ais.views import view_api_redirect_notam


urlpatterns = [
    path('',view_panel_aroaislp, name="view_panel_aroaislp"),
    
    path('nof',view_panel_notaminternacional, name="view_panel_notaminternacional"),
    path('asunto8126',view_getAsunto, name="view_getAsunto"),
    path('estado_asunto8126',view_getEstadoAsunto, name="view_getEstadoAsunto"),

    path('slcb/', view_ais_for_aed, name="view_panel_aisslcb"),
    path('slvr/', view_ais_for_aed, name="view_panel_aisslvr"),
    path('sltr/', view_ais_for_aed, name="view_panel_aissltr"),
    
    path('aroaisfpl/',view_admin_ais, name='view_admin_ais'),
    
    path('pibautomatizado/', view_pib_automatizado, name="view_pib_automatizado"), #
    path('archivarpib/', view_archivar_pib, name="view_archivar_pib"), #archiva pib
    path('publicarguardar/', view_publicarguardar_pib, name="view_publicarguardar_pib"), #archiva pib
    path('pibtiemporeal/', view_pib_tiemporeal, name="view_pib_tiemporeal"), #archiva pib
    
    path('pibtiemporeal2/', view_pib_tiemporeal2, name="view_pib_tiemporeal2"), #archiva pib
    
    path('verpib/', view_pibupdate_tiemporeal, name="view_pibupdate_tiemporeal"), #envia al frontend datos actualizados
    path('guardarregistropib/', view_guardarregistro_pib, name="view_guardarregistro_pib"), #envia al frontend datos actualizados
    path('imprimirpib/', view_imprimir_pibrealtime, name="view_imprimir_pibrealtime"), #INTERFAZ PARA IMPRIMIR EL PIB
    path('newnotam/', view_new_notam, name="view_new_notam"), #SIMULADOR GENERADOR DE NOTAM

    path('newnotam2/', view_new_notam_2, name="view_new_notam_2"), #SIMULADOR GENERADOR DE NOTAM

    path('codigos_abreviaturas/', view_codigos_abreviaturas, name="view_codigos_abreviaturas"), #SIMULADOR GENERADOR DE NOTAM


    ## CODIGOS Y ABREVIATURAS
    path('responseabreviatura/', view_get_abreviatura8400, name="view_get_abreviatura8400"), #
    path('response8126/', view_get_codigo8126, name="view_get_codigo8126"), #
    path('responseLetter8126/', view_get_lista_asuntos_8126, name="view_get_lista_asuntos_8126"), #
    path('responseEstados8126/', view_get_lista_estados_8126, name="view_get_lista_estados_8126"), #

    ## OBTENIENDO CORRELATIVO    
    path('correlativocharlie/', view_get_correlativo_charly, name="view_get_correlativo_charly"), #
    path('correlativoalpha/', view_get_correlativo_alfa, name="view_get_correlativo_alfa"), #


    ## API PARA CONSUMO DE HISTORIALES NOTAM NEW, REPLA, CANCEL
    path('charlyfrom_notamn/', api_historico_charly_from_notamn, name="api_historico_charly_from_notamn"), #
    path('charlyfrom_notamr/', api_historico_charly_from_notamr, name="api_historico_charly_from_notamr"), #
    path('charlyfrom_notamc/', api_historico_charly_from_notamc, name="api_historico_charly_from_notamc"), #


    path('alfafrom_notamn/', api_historico_alfa_from_notamn, name="api_historico_alfa_from_notamn"), #
    path('alfafrom_notamr/', api_historico_alfa_from_notamr, name="api_historico_alfa_from_notamr"), #
    path('alfafrom_notamc/', api_historico_alfa_from_notamc, name="api_historico_alfa_from_notamc"), #

    path('allnotams/',view_todos_notams, name='view_todos_notams'),
    path('banconotam/',view_banco_notam, name='view_banco_notam'),

    path('view_charlie/<path:id_notam>/',view_notam_modal_charly, name='view_notam_modal_charly'),
    path('view_alpha/<path:id_notam>/',view_notam_modal_alfa, name='view_notam_modal_alfa'),
    

    ## API PARA GUARDAR NOTAM CREADO
    path('createnotam/', view_post_crear_notam, name="view_post_crear_notam"), #
    
    ## API PARA BUSCAR NOTA POR RANGO
    path('notamsearch/', view_api_notam_search, name="view_api_notam_search"), #
    

    ## API PARA BUSCAR NOTA POR CADENA
    path('notamstring/', view_api_notam_search_string, name="view_api_notam_search_string"), #
    

    ##API PARA CONSULTAR AED GEOREFERENCIADOS
    path('georefaed/', view_get_aed_georef, name="view_get_aed_georef"), #
    
    
    
    path('recuperar_notam/', view_api_redirect_notam, name="view_api_redirect_notam"), #
    
]
