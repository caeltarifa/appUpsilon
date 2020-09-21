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

from django.urls import path, include
from django.contrib import admin

#vistas para la pagina principal
from .views import view_pagina_principal#, control_acceso_login

#paginas de la aplicacion "plan_vuelo"
#from apps.plan_vuelo.views import post_detail


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view_pagina_principal,name='view_pagina_principal'),
    
    path('generacion_fpl/', include('apps.generacion_fpl.urls')),
    path('plan_vuelo/', include('apps.plan_vuelo.urls')),
    #path('plan_vuelo/postdetail/<int:pk>/', post_detail , name='post_detail')
    #path('accounts/login/', control_acceso_login ,name='acceso_login'),
]


#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
