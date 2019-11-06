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
from .views import view_pagina_principal

#paginas de la aplicacion "plan_vuelo"
#from apps.plan_vuelo.views import post_detail


urlpatterns = [
    path('', view_pagina_principal,name='index_principal'),
    path('admin/', admin.site.urls),
    
    path('plan_vuelo/', include('apps.plan_vuelo.urls')),
    #path('plan_vuelo/postdetail/<int:pk>/', post_detail , name='post_detail')
]


#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
