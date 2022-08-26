from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin

from django import forms
from apps.mantenimiento.models import Mantenimiento
from django.contrib.auth.models import User

from apps.usuario.models import Perfil

#------------------------------------ Opciones de campos select --------------------
tipo_mante2 = (('Tecnologico','Tecnologico'),('Audiovisual','Audiovisual'))
tipo_mante = (('Soporte Técnico','Soporte Técnico'),('Soporte Técnico','Soporte Técnico'))
#------------------------------------ Formulario para Generar Ficha -----------------------------

class Ficha_Registrar_Form(forms.ModelForm):
    tipo_equipo_man = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control text-capitalize',
                'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()",
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+'
                }),
                label='Marca del Equipo')

    tipo_man = forms.ChoiceField(
        choices=tipo_mante, 
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                }),
                label='Tipo de Mantenimiento')

    marca_equipo_man = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()",
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+'
                }),
                label='Marca del Equipo')

    modelo_equipo_man = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+'
                }),
                label='Modelo del Equipo')

    accesorios_equipo_man = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()", 
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+',
                'rows':'2'
                }),
                label='Accesorios del Equipo')

    class Meta:
        model = Mantenimiento
        
        fields = {
        'cliente','usuario','falla_equipo_man','tipo_equipo_man','tipo_man','marca_equipo_man','modelo_equipo_man','accesorios_equipo_man',
        }
        widgets = {
            'cliente': AutocompleteSelect(
            Mantenimiento._meta.get_field('cliente').remote_field,
            admin.site,
            attrs={'placeholder': 'seleccionar...'},
            ),
            'usuario': AutocompleteSelect(
            Mantenimiento._meta.get_field('usuario').remote_field,
            admin.site,
            attrs={'placeholder': 'seleccionar...'},
            ),
            'falla_equipo_man' : forms.Textarea(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+',
                'rows':'2'
                }),
        }


#------------------------------------ Formulario para Generar Ficha -----------------------------

class Ficha_Editar_Form(forms.ModelForm):
    tipo_equipo_man = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()",
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+'
            }),
            label='Marca del Equipo')

    tipo_man = forms.ChoiceField(
        choices=tipo_mante, 
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }),
            label='Tipo de Mantenimiento')

    marca_equipo_man = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()",
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+'
            }),
            label='Marca del Equipo')

    modelo_equipo_man = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+'
            }),
            label='Modelo del Equipo')

    accesorios_equipo_man = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()", 
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+',
                'rows':'2'
            }),
            label='Accesorios del Equipo')

    procedimiento_man = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+',
                'rows':'2'
            }),
            label='Procedimientos del Tecnico')

    observaciones_man = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+',
                'rows':'2'
            }),
            label='Observaciones del Tecnico')
    
    costo_man = forms.FloatField(
        min_value=0,
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }),
            label='Costo del Mantenimiento')
    

    class Meta:
        model = Mantenimiento
        
        fields = {
        'cliente','usuario',
        'falla_equipo_man','tipo_equipo_man','tipo_man',
        'marca_equipo_man','modelo_equipo_man','accesorios_equipo_man',
        'estado_man','costo_man',
        'procedimiento_man', 'observaciones_man',
        }
        widgets = {
            'cliente': AutocompleteSelect(
            Mantenimiento._meta.get_field('cliente').remote_field,
            admin.site,
            attrs={'placeholder': 'seleccionar...'},
            ),
            'usuario': AutocompleteSelect(
            Mantenimiento._meta.get_field('usuario').remote_field,
            admin.site,
            attrs={'placeholder': 'seleccionar...'},
            ),
            'falla_equipo_man' : forms.Textarea(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+',
                'rows':'2'}
            ),
            'estado_man': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


#todo============================================================================================
#todo-------------------------------- Formulario para Generar Ficha -----------------------------
#todo============================================================================================

class Ficha_Gestion_Form(forms.ModelForm):
    costo_man = forms.FloatField(
        min_value=0,
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }),
            label='Costo del Mantenimiento')
    class Meta:
        model = Mantenimiento
        
        fields = {
            'estado_man','costo_man',
        }
        widgets = {
            'estado_man': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }


#todo============================================================================================
#todo------------------------------ Formulario para Finalizar Ficha -----------------------------
#todo============================================================================================

class Ficha_Finalizar_Form(forms.ModelForm):
    
    procedimiento_man = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+',
                'rows':'2'
            }),
            label='Procedimientos del Tecnico')

    observaciones_man = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+',
                'rows':'2'
            }),
            label='Observaciones del Tecnico')

    costo_man = forms.FloatField(
        min_value=0,
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step':".01",
            }),
            label='Costo del Mantenimiento')

    class Meta:
        model = Mantenimiento
        
        fields = {
            'procedimiento_man', 'observaciones_man', 'costo_man',
        }


#todo============================================================================================
#todo-------------------------------- Formulario para Entregar Equipo ---------------------------
#todo============================================================================================

class Ficha_Entrega_Form(forms.ModelForm):
    costo_man = forms.FloatField(
        min_value=0,
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step':".01",
            }),
            label='Costo del Mantenimiento')
    class Meta:
        model = Mantenimiento
        
        fields = {
            'costo_man',
        }