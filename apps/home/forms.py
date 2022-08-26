from django import forms
from django.contrib.auth.models import User

from apps.usuario.models import Perfil

#-------------- Formulario para contactenos -----------------
# A form that will be used to send an email to the admin.
class Contacto_form(forms.Form):
    nombre_completo = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control border-0 text-uppercase',
                'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()",
                'id': 'form2Example1', 
                'pattern':'[A-Za-záéíóú:, ,]+', 
                'onkeydown':"return /[A-Za-záéíóú, ,]/i.test(event.key)",
                'style':'height: 55px',
                'placeholder':'Nombre Completo',
                }),
                label='Nombre Completo')

    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'type':'email',
                'class':'form-control border-0',
                'id':'registerEmail',
                'style':'height: 55px',
                'placeholder':'Correo Electrónico',
                }),
                label='Email')

    telefono = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control border-0',
                'rows':'5',
                'style':'height: 55px',
                'placeholder':'Numero de Teléfono',
                'type':'tel',
                'id': 'form6Example6',
                'oninput':"this.value = this.value.replace(/[^0-9-]/g, '').replace(/(\..*?)\..*/g, '$1');"
                }),
                label='Número de contacto')

    mensaje = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control border-0 text-capitalize', 
                'id': 'form4Example3', 
                'rows':'5',
                'placeholder':'Consulta',
                }),
                label='Mensaje a enviar')



#todo------------------- Formulario para reportes de Clientes-------------------

Meses = (('0','Todos los Meses'),('1','Enero'),('2','Febrero'),('3','Marzo'),('4','Abril'),('5','Mayo'),('6','Junio'),('7','Julio'),('8','Agosto'),('9','Septiembre'),('10','Octubre'),('11','Noviembre'),('12','Diciembre'))
Estados = (('0','Todos los estados'),('1','Ingresado'),('2','En Proceso'),('3','Finalizado'),('4','Entregado'))

class Reporte_form(forms.Form):
    #fecha_entrega = forms.DateTimeField(required=True, widget = forms.DateTimeInput(format=('%d-%m-%Y'),attrs={'class': 'form-control', 'placeholder': 'Selecciona una fecha','type': 'date'}),label='Fecha de reporte', help_text="El formato es: 24/12/2020")
    meses = forms.ChoiceField(
        choices=Meses, required=True, 
        widget=forms.Select(
            attrs={
                'class': 'form-control browser-default custom-select',
                'placeholder': 'Selecciona un mes',
                })
                ,label='Seleccione un mes del año')

    year = forms.FloatField(
        min_value=2020,
        max_value=2099,
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': "1",
                'autofocus':'true',
                'placeholder': 'Ingrese un año',
            }),
            label='Costo del Mantenimiento')



#todo------------------- Formulario para reportes de los tecnicos -------------------

class Reporte_form_tecnico(forms.Form):
    #fecha_entrega = forms.DateTimeField(required=True, widget = forms.DateTimeInput(format=('%d-%m-%Y'),attrs={'class': 'form-control', 'placeholder': 'Selecciona una fecha','type': 'date'}),label='Fecha de reporte', help_text="El formato es: 24/12/2020")
    meses = forms.ChoiceField(
        choices=Meses, required=True, 
        widget=forms.Select(
            attrs={
                'class': 'form-control browser-default custom-select',
                'placeholder': 'Selecciona un mes',
                })
                ,label='Seleccione un mes del año')

    year = forms.FloatField(
        min_value=2020,
        max_value=2099,
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': "1",
                'autofocus':'true',
                'placeholder': 'Ingrese un año',
            }),
            label='Costo del Mantenimiento')
    
    tecnico = forms.ModelChoiceField(
        queryset=Perfil.objects.filter(cargo_perfil__icontains = 'Técnico' ),
        empty_label="Todos los Tecnicos",
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control browser-default custom-select',
                })
        )


#todo------------------- Formulario para reportes de las fichas de mantenimiento -------------------

class Reporte_form_ficha(forms.Form):
    #fecha_entrega = forms.DateTimeField(required=True, widget = forms.DateTimeInput(format=('%d-%m-%Y'),attrs={'class': 'form-control', 'placeholder': 'Selecciona una fecha','type': 'date'}),label='Fecha de reporte', help_text="El formato es: 24/12/2020")
    meses = forms.ChoiceField(
        choices=Meses, required=True, 
        widget=forms.Select(
            attrs={
                'class': 'form-control browser-default custom-select',
                'placeholder': 'Selecciona un mes',
                })
                ,label='Seleccione un mes del año')

    year = forms.FloatField(
        min_value=2020,
        max_value=2099,
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': "1",
                'autofocus':'true',
                'placeholder': 'Ingrese un año',
            }),
            label='Costo del Mantenimiento')
    '''
    estados = forms.ChoiceField(
        choices=Estados, required=True, 
        widget=forms.Select(
            attrs={
                'class': 'form-control browser-default custom-select',
                'placeholder': 'Selecciona un estado',
                })
                ,label='Seleccione un estado ')'''


#todo------------------- Formulario para consultar las fichas de mantenimiento -------------------

class form_consulta_ficha(forms.Form):
    codigo_ficha = forms.CharField(
        required=True,
        max_length=10,
        min_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control border-0', 
                'id': 'form2Example1', 
                'pattern':'[A-Za-záéíóú:, ,--,@,_,[0-9]+',
                'style':'height: 55px; border:1px solid !important;',
                'placeholder':'Ingrese el código de la Ficha',
                'autofocus':''
                }),
                label='Código de la Ficha de Mantenimiento')