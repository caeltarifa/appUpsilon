from django.contrib import admin

from apps.plan_vuelo.models import Empresa_institucion,Flp_trafico,Ruta_flp,EntrePuntos_flp, Ruta_guardada,Cargo,Trabajador,Flp_aprobado, Punto_satelital, Notam_trafico, Aeropuerto

# Register your models here.
admin.site.register(Empresa_institucion)
admin.site.register(Flp_trafico)
#admin.site.register(Metar_trafico)
admin.site.register(Ruta_flp)
admin.site.register(EntrePuntos_flp)
admin.site.register(Ruta_guardada)
admin.site.register(Cargo)
admin.site.register(Trabajador)
admin.site.register(Flp_aprobado)
admin.site.register(Punto_satelital)
admin.site.register(Notam_trafico)
admin.site.register(Aeropuerto)