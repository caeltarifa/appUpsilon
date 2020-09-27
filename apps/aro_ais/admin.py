from django.contrib import admin

# Register your models here.


from apps.aro_ais.models import Pib_trafico
from apps.aro_ais.models import Pib_extenso

admin.site.register(Pib_trafico)
admin.site.register(Pib_extenso)
