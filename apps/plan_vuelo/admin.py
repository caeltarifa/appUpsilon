from django.contrib import admin

from apps.plan_vuelo.models import Flp_trafico, Metar_trafico, Trabajadores, Flp_aprobado, Ruta_flp, EntrePuntos_flp


# Register your models here.
admin.site.register(Flp_trafico)
admin.site.register(Metar_trafico)
admin.site.register(Trabajadores)
admin.site.register(Flp_aprobado)
admin.site.register(Ruta_flp)
admin.site.register(EntrePuntos_flp)


