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


admin.site.register(Pib_trafico)
admin.site.register(Pib_extenso)
admin.site.register(Pib_registro_documento)
admin.site.register(Letra_asunto)
admin.site.register(Asunto)
admin.site.register(Estado_asunto)
admin.site.register(Simbolo_8400)
admin.site.register(Abreviatura_8400)
admin.site.register(Significado_8400)