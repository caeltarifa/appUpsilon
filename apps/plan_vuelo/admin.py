from django.contrib import admin

from apps.plan_vuelo.models import Empresa_institucion,Flp_trafico,Metar_trafico,Ruta_flp,EntrePuntos_flp,Cargo,Trabajador,Flp_aprobado

# Register your models here.
admin.site.register(Empresa_institucion)
admin.site.register(Flp_trafico)
admin.site.register(Metar_trafico)
admin.site.register(Ruta_flp)
admin.site.register(EntrePuntos_flp)
admin.site.register(Cargo)
admin.site.register(Trabajador)
admin.site.register(Flp_aprobado)


