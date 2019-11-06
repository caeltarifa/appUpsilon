from django import forms

# from apps.plan_vuelo.models import Plan_vuelo

# class Vuelo_Aprobado_form(forms.ModelForm):

#     class meta:
#         model = Plan_vuelo

#         fields = [
#             'estadomsj',
#             'hora',
#             'plan_vuelo',
#             'tipo_avion',
#             'origen',
#             'destino',
#             'hora_salida',
#             'regla_vuelo',
#             'linea_aerea',
#         ]

#         labels = {
#             'estadomsj': 'Estadomsj',
#             'hora': 'Hora',
#             'plan_vuelo': 'Plan_vuelo',
#             'tipo_avion': 'Tipo_avion',
#             'origen': 'Origen',
#             'destino': 'Destino',
#             'hora_salida': 'Hora_salida',
#             'regla_vuelo': 'Regla_vuelo',
#             'linea_aerea': 'Linea_aerea',
#         }

#         widgets = {
#             'estadomsj': forms.DateTimeInput(attrs={'class': 'form-control'}),
#             'hora': forms.TextInput(attrs={'class': 'form-control'}),
#             'plan_vuelo': forms.TextInput(attrs={'class': 'form-control'}),
#             'tipo_avion': forms.DateTimeInput(attrs={'class': 'form-control'}),
#             'origen': forms.TextInput(attrs={'class': 'form-control'}),
#             'destino': forms.TextInput(attrs={'class': 'form-control'}),
#             'hora_salida':forms.TextInput(attrs={'class': 'form-control'}),
#             'regla_vuelo':forms.TextInput(attrs={'class': 'form-control'}),
#             'linea_aerea':forms.TextInput(attrs={'class': 'form-control'}),
#         }

# class PostForm(forms.ModelForm):
#     class Meta:
#         model= Plan_vuelo
#         fields = (
#             'estadomsj',
#             'hora',
#             'plan_vuelo',
#             'tipo_avion',
#             'origen',
#             'destino',
#             'hora_salida',
#             'regla_vuelo',
#             'linea_aerea',
#         )
