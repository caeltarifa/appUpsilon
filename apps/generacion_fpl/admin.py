from django.contrib import admin

from apps.generacion_fpl.models import Comunicacional,Estado,Operacional,Suplementaria,Plan_vuelo_presentado

# Register your models here.
admin.site.register(Comunicacional)
admin.site.register(Estado)
admin.site.register(Operacional)
admin.site.register(Suplementaria)
admin.site.register(Plan_vuelo_presentado)
