from django.contrib import admin

# Register your models here.
from apps.trabajadoresATS.models import TrabajadoresATS,CuentasATS

# Register your models here.
admin.site.register(TrabajadoresATS)
admin.site.register(CuentasATS)
