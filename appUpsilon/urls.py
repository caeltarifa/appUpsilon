"""appUpsilon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf.urls import url, include

from django.urls import path, include
from django.contrib import admin



from django.conf import settings
from django.conf.urls.static import static

# vistas para la pagina principal
from .views import view_pagina_principal  # , control_acceso_login

from .views import view_panel_comunicaciones, view_admin_comunicaciones

from .views import view_pib_tiempo_real
from .views import api_get_notam_aeropuerto

from .views import api_search_data_notam

# paginas de la aplicacion "plan_vuelo"
#from apps.plan_vuelo.views import post_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view_pagina_principal, name='view_pagina_principal'),
    path('generacion_fpl/', include('apps.generacion_fpl.urls')),
    path('plan_vuelo/', include('apps.plan_vuelo.urls')),
    path('ais/', include('apps.aro_ais.urls')),

    #path('plan_vuelo/postdetail/<int:pk>/', post_detail , name='post_detail')
    #path('accounts/login/', view_pagina_principal ,name='acceso_login'),

    #url('accounts/login/', view_pagina_principal),

    url('^comunicaciones$', view_panel_comunicaciones,
        name='view_panel_comunicaciones'),
    url('^comunicaciones$', view_admin_comunicaciones,
        name='view_admin_comunicaciones'),

    # PIB EN TIEMPO REAL
    path('pibrealtime/', view_pib_tiempo_real, name='view_pib_tiempo_real'),
    path('icao_notam/', api_get_notam_aeropuerto, name='api_get_notam_aeropuerto'),


    path('rqn_notam/', api_search_data_notam, name='api_search_data_notam'),
    

]


# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#CHANGIN THE DJANGO ADMINISTRATION

admin.site.site_header = "IFIS NUKLEAR - AASANA"
admin.site.site_title = "IFIS NUKLEAR AASANA"
admin.site.index_title = "Sitio de administración de datos"

