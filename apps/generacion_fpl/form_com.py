from django import forms

from apps.generacion_fpl.models import Comunicacional, Operacional, Suplementaria, Plan_vuelo_presentado

from apps.plan_vuelo.models import Trabajador

from datetime import datetime

choices_reglas = [('1','I'),('2','V'),('3','Y'),('4','Z')]
choices_tipo_vuelo = [('1','S'),('2','N'),('3','G'),('4','M'),('5','X')]
choices_turbulenta = [('1','L'),('2','M'),('3','H')]

class  ComunicacionalForm(forms.ModelForm):
    class Meta:
        model=Comunicacional

        fields=[
            'direcciones_amhs',
            'originador_amhs',
            'fecha_hora_deposito',
            'tiempo_utc_modific',
        ]

        labels={
            'direcciones_amhs': 'direcciones_amhs',
            'originador_amhs': 'originador_amhs',
            'fecha_hora_deposito': 'fecha_hora_deposito',
            'tiempo_utc_modific': 'tiempo_utc_modific',
        }

        widgets={
            'direcciones_amhs': forms.Textarea(attrs={'class':'form-control','id':"destinatarios", 'rows':"2", 'cols':"80", 'type':"text", 'style':"font-family:Verdana;font-size: 13px;"}),
            'originador_amhs': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_hora_deposito': forms.TextInput(attrs={'class':'form-control'}),
            'tiempo_utc_modific': forms.TextInput(attrs={'class':'form-control'}),
        }

class  OperacionalForm(forms.ModelForm):
    class Meta:
        model=Operacional

        fields=[
            'id_aeronave',
            'regla_vuelo',
            'tipo_vuelo',
            'numero',
            'tipo_aeronave',
            'estela_turbulenta',
            'equipoA',
            'equipoB',
            'aerodromo_salida',
            'hora_salida',
            'velocidad_crucero_cat',
            'velocidad_crucero',
            'nivel_cat',
            'nivel',
            'ruta',
            'aerodromo_destino',
            'total_eet',
            'aerodromo_alterno',
            'aerodromo_alterno2',
            'otros_datos',
        ]

        labels={
            'id_aeronave':'id_aeronave',
            'regla_vuelo':'regla_vuelo',
            'tipo_vuelo':'tipo_vuelo',
            'numero':'numero',
            'tipo_aeronave':'tipo_aeronave',
            'estela_turbulenta':'estela_turbulenta',
            'equipoA':'equipoA',
            'equipoB':'equipoB',
            'aerodromo_salida':'aerodromo_salida',
            'hora_salida':'hora_salida',
            'velocidad_crucero_cat':'velocidad_crucero_cat',
            'velocidad_crucero':'velocidad_crucero',
            'nivel_cat':'nivel_cat',
            'nivel':'nivel',
            'ruta':'ruta',
            'aerodromo_destino':'aerodromo_destino',
            'total_eet':'total_eet',
            'aerodromo_alterno':'aerodromo_alterno',
            'aerodromo_alterno2':'aerodromo_alterno2',
            'otros_datos':'otros_datos',
        }

        widgets={
            'id_aeronave':forms.TextInput(attrs={'id':"identif_aeronave", 'name':"numeroVuelo", 'onKeyUp':"this.value=this.value.toUpperCase();",'size':"7", 'maxlength':"7", 'type':"text"}),
            'regla_vuelo':forms.Select(choices=[('1','I'),('2','V'),('3','Y'),('4','Z')],attrs={'id':"regla_vuelo"}),
            'tipo_vuelo':forms.Select(choices=[('1','S'),('2','N'),('3','G'),('4','M'),('5','X')],attrs={'id':"tipo_vuelo"}),
            'numero':forms.NumberInput(attrs={'id':"numero", 'name':"numero", 'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"2", 'maxlength':"2", 'type':"text"}),
            'tipo_aeronave':forms.TextInput(attrs={'id':"tipoAeronave", 'name':"tipoAeronave", 'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"4", 'maxlength':"4", 'type':"text"}),
            'estela_turbulenta':forms.Select(choices=[('1','L'),('2','M'),('3','H')]),
            'equipoA':forms.TextInput(attrs={'id':"equipoA", 'name':"equipoA", 'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"18", 'type':"text"}),
            'equipoB':forms.TextInput(attrs={'id':"equipoB", 'name':"equipoB", 'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"10", 'type':"text"}),
            'aerodromo_salida':forms.TextInput(attrs={'id':"aerodromo_salida", 'name':"aedDep", 'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"4", 'maxlength':"4", 'type':"text"}),
            'hora_salida':forms.TextInput(attrs={'id':"hora_salida", 'name':"etd", 'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"4", 'maxlength':"4", 'type':"text"}),
            #velocidad:crucero:categora
            'velocidad_crucero_cat':forms.Select(choices=[('1','N'),('2','M'),('3','K')]),
            'velocidad_crucero':forms.TextInput(attrs={'id':"velocidad_crucero_numero", 'name':"velocidadCrucero", 'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"4", 'maxlength':"4", 'type':"text"}),
            #nivel categorico
            'nivel_cat':forms.Select(choices=[('1','F'),('2','A'),('3','S'),('4','M')]),
            'nivel':forms.TextInput(attrs={'id':"nivel_numero", 'name':"nivel", 'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"4", 'maxlength':"4", 'type':"text"}),
            'ruta':forms.Textarea(attrs={'id':"ruta", 'name':"ruta", 'onKeyUp':"this.value=this.value.toUpperCase();", 'onKeyPress':"if (event.keyCode == 13 || event.charCode == 45) return false;",  'rows':"3", 'cols':"60", 'type':"text", 'style':"font-family:Verdana;font-size: 13px;"}),
            'aerodromo_destino':forms.TextInput(attrs={'id':"aerodromo_destino", 'name':"aedArr",  'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"4", 'maxlength':"4", 'type':"text"}),
            'total_eet':forms.TextInput(attrs={'id':"eet_total", 'name':"eet", 'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"4", 'maxlength':"4", 'type':"text"}),
            'aerodromo_alterno':forms.TextInput(attrs={'id':"aerod_ater1", 'name':"aedAlt1", 'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"4", 'maxlength':"4", 'type':"text"}),
            'aerodromo_alterno2':forms.TextInput(attrs={'id':"aerod_ater2", 'name':"aedAlt2", 'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"4", 'maxlength':"4", 'type':"text"}),
            'otros_datos':forms.Textarea(attrs={'id':"otros_datos", 'name':"otrosDatos", 'onKeyUp':"this.value=this.value.toUpperCase();", 'onKeyPress':"if (event.keyCode == 13 || event.charCode == 45) return false;",  'rows':"3", 'cols':"65", 'type':"text", 'style':"font-family:Verdana;font-size: 13px;"}),
        }


class  SuplementariaForm(forms.ModelForm):
    class Meta:
        model=Suplementaria

        fields=[
            'autonomia_hr_min',
            'personas_bordo',
            'equipo_radio_uhf',
            'equipo_radio_vhf',
            'equipo_radio_elt',
            'equipo_superv',
            'equipo_superv_polar',
            'equipo_superv_deser',
            'equipo_superv_mar',
            'equipo_superv_jung',
            'chaleco',
            'chaleco_luz',
            'chaleco_fluor',
            'chaleco_uhf',
            'chaleco_vhf',
            'nro_botes',
            'capacidad_botes',
            'color_bote',
            'color_marca_avion',
            'obs',
            'piloto',
            'requisitos_adic',
        ]

        labels={
            'autonomia_hr_min':'autonomia_hr_min',
            'personas_bordo':'personas_bordo',
            'equipo_radio_uhf':'equipo_radio_uhf',
            'equipo_radio_vhf':'equipo_radio_vhf',
            'equipo_radio_elt':'equipo_radio_elt',
            'equipo_superv':'equipo_superv',
            'equipo_superv_polar':'equipo_superv_polar',
            'equipo_superv_deser':'equipo_superv_deser',
            'equipo_superv_mar':'equipo_superv_mar',
            'equipo_superv_jung':'equipo_superv_jung',
            'chaleco':'chaleco',
            'chaleco_luz':'chaleco_luz',
            'chaleco_fluor':'chaleco_fluor',
            'chaleco_uhf':'chaleco_uhf',
            'chaleco_vhf':'chaleco_vhf',
            'nro_botes':'nro_botes',
            'capacidad_botes':'capacidad_botes',
            'color_bote':'color_bote',
            'color_marca_avion':'color_marca_avion',
            'obs':'obs',
            'piloto':'piloto',
            'requisitos_adic':'requisitos_adic',
        }

        widgets={
            'autonomia_hr_min':forms.TextInput(attrs={'id':"autonomia_hr_min", 'size':"4", 'maxlength':"4", 'type':"text"}),
            'personas_bordo':forms.TextInput(attrs={'id':"personas_bordo",'size':"3", 'maxlength':"3"}),
            'equipo_radio_uhf':forms.CheckboxInput(attrs={'id':"equipo_radio_uhf"}),
            'equipo_radio_vhf':forms.CheckboxInput(attrs={'id':"equipo_radio_vhf"}),
            'equipo_radio_elt':forms.CheckboxInput(attrs={'id':"equipo_radio_elt"}),
            'equipo_superv':forms.CheckboxInput(attrs={'id':"equipo_superv"}),
            'equipo_superv_polar':forms.CheckboxInput(attrs={'id':"equipo_superv_polar"}),
            'equipo_superv_deser':forms.CheckboxInput(attrs={'id':"equipo_superv_deser"}),
            'equipo_superv_mar':forms.CheckboxInput(attrs={'id':"equipo_superv_mar"}),
            'equipo_superv_jung':forms.CheckboxInput(attrs={'id':"equipo_superv_jung"}),
            'chaleco':forms.CheckboxInput(attrs={'id':"chaleco"}),
            'chaleco_luz':forms.CheckboxInput(attrs={'id':"chaleco_luz"}),
            'chaleco_fluor':forms.CheckboxInput(attrs={'id':"chaleco_fluor"}),
            'chaleco_uhf':forms.CheckboxInput(attrs={'id':"chaleco_uhf"}),
            'chaleco_vhf':forms.CheckboxInput(attrs={'id':"chaleco_vhf"}),
            'nro_botes':forms.TextInput({'id':"nro_botes",'size':"2", 'maxlength':"2"}),
            'capacidad_botes':forms.TextInput(attrs={'id':"capacidad_botes",'size':"3", 'maxlength':"3"}),
            'color_bote':forms.TextInput(attrs={'id':"color_bote",'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"20", 'maxlength':"20"}),
            'color_marca_avion':forms.TextInput(attrs={'id':"color_marca_avion",'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"90", 'maxlength':"90"}),
            'obs':forms.TextInput(attrs={'id':"obs",'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"70", 'maxlength':"70"}),
            'piloto':forms.TextInput(attrs={'id':"piloto",'onKeyUp':"this.value=this.value.toUpperCase();", 'size':"50", 'maxlength':"50"}),
            'requisitos_adicionales':forms.Textarea({'id':"requisitos_adicionales",'rows':"2", 'cols':"25", 'style':"border: none;font-family:Verdana;font-size: 13px;"}),
        }

class  Plan_presentadoForm(forms.ModelForm):
    class Meta:
        model=Plan_vuelo_presentado

        fields=[
            'nro_formulario',
            'fk_despachador',
            'fk_estado',
            'fecha_presentacion',
            'hora_presentacion',
        ]

        labels={
            'nro_formulario':'nro_formulario',
            'fk_despachador': 'fk_despachador',
            'fk_estado':'fk_estado',
            'fecha_presentacion':'fecha_presentacion',
            'hora_presentacion':'hora_presentacion',
        }

        widgets={
            'nro_formulario':forms.TextInput(attrs={'id':"numeroForm", 'size':'1', 'style':'text-align:right;'}),
            'fk_despachador': forms.TextInput(attrs={'id':"despachador", 'value':'dato', 'size':'7', 'style':'text-align:right;'}),
            'fk_estado':forms.TextInput(attrs={'id':"estado", 'value':'7', 'size':'7', 'style':'text-align:right;'}),
            'fecha_presentacion':forms.TextInput(attrs={'id':"fechaForm", 'size':'7', 'style':'text-align:right;'}),
            'hora_presentacion':forms.TextInput(attrs={'id':"horaForm", 'size':'5', 'style':'text-align:right;'}),
            
            #'fk_despachador': forms.Select(queryset=Trabajador.objects.filter(empresa_institucion_id=id_empresa)),
        }
