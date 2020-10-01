from django.conf.urls import url, include
from django.urls import path, re_path

# ARO AIS ################################################################################################################
from apps.aro_ais.views import view_admin_ais, view_panel_aroais,view_pib_automatizado, view_archivar_pib, view_publicarguardar_pib, view_pib_tiemporeal,view_pibupdate_tiemporeal

urlpatterns = [
    path('',view_panel_aroais, name="view_panel_aroais"),
    
    path('aroaisfpl/',view_admin_ais, name='view_admin_ais'),
    
    path('pibautomatizado/', view_pib_automatizado, name="view_pib_automatizado"), #
    path('archivarpib/', view_archivar_pib, name="view_archivar_pib"), #archiva pib
    path('publicarguardar/', view_publicarguardar_pib, name="view_publicarguardar_pib"), #archiva pib
    path('pibtiemporeal/', view_pib_tiemporeal, name="view_pib_tiemporeal"), #archiva pib
    path('verpib/', view_pibupdate_tiemporeal, name="view_pibupdate_tiemporeal"), #envia al frontend datos actualizados
]