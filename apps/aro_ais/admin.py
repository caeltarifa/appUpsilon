from django.contrib import admin

# Register your models here.


from apps.aro_ais.models import Pib_trafico
from apps.aro_ais.models import Pib_extenso
from apps.aro_ais.models import Pib_registro_documento
from apps.aro_ais.models import Letra_asunto
from apps.aro_ais.models import Asunto
from apps.aro_ais.models import Estado_asunto
from apps.aro_ais.models import Simbolo_8400
from apps.aro_ais.models import Abreviatura_8400
from apps.aro_ais.models import Significado_8400
from apps.aro_ais.models import Historico_pib

from apps.aro_ais.models import Direccion_amhs
from apps.aro_ais.models import Prioridad
from apps.aro_ais.models import Tipo_notam
from apps.aro_ais.models import Serie_notam
from apps.aro_ais.models import Banco_notam_charly


from apps.plan_vuelo.models import Notam_trafico_resumen
from apps.plan_vuelo.models import Pib_tiempo_real


admin.site.register(Pib_trafico)
admin.site.register(Pib_extenso)
admin.site.register(Pib_registro_documento)
admin.site.register(Letra_asunto)
admin.site.register(Asunto)
admin.site.register(Estado_asunto)
admin.site.register(Simbolo_8400)
admin.site.register(Abreviatura_8400)
admin.site.register(Significado_8400)
admin.site.register(Historico_pib)

admin.site.register(Direccion_amhs)
admin.site.register(Prioridad)
admin.site.register(Tipo_notam)
admin.site.register(Serie_notam)
admin.site.register(Banco_notam_charly)


admin.site.register(Notam_trafico_resumen)
admin.site.register(Pib_tiempo_real)