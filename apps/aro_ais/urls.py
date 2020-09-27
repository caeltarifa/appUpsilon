from django.conf.urls import url, include
from django.urls import path, re_path

# ARO AIS ################################################################################################################
from apps.aro_ais.views import view_panel_aroais


urlpatterns = [
    path('aroais/', view_panel_aroais, name="view_panel_aroais"), #redirije al panel de control de aroais
    
]