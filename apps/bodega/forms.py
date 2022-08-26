from dataclasses import fields
import numbers
from django import forms

from apps.bodega.models import Bodega
# -------------formulario para elementos de bodega--------------


class Bodega_form(forms.ModelForm):
    nombre_pieza = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
              'class': 'form-control text-uppercase', 
              'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()",
                'pattern':'[A-Za-z, ,]+', 
                'onkeydown':"return /[A-Za-záéíóú, ,]/i.test(event.key)",
                'placeholder':'Ingrese el nombre del equipo o pieza',
                'type':'text',
            }),
            label="Nombre del equipo o pieza")
    descripcion_pieza = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
              'class': 'form-control text-capitalize', 
                'pattern':'[A-Za-z0-9áéíóú:, ,]+', 
                'onkeydown':"return /[A-Za-záéíóú, ,]/i.test(event.key)",
                'placeholder':'Ingrese una pequeña descripción del equipo o pieza',
                'type':'text',
                'rows':'4',
            }),
            label="Descripción")
    serie_pieza = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
              'class': 'form-control', 
              'pattern':'[A-Za-z0-9_-]', 
              'onkeydown':"return /[A-Za-z0-9,_-]/i.test(event.key)",
              'placeholder':'Ingrese el número de serie o modelo',
              'type':'text',
              'rows':'1',
            }),
            label="Número de Serie del equipo o pieza")
    cantidad_pieza = forms.IntegerField(
        required=True,
        min_value=1,
        max_value=50000,
        widget=forms.NumberInput(
            attrs={
              'class': 'form-control',
              'placeholder':'Número de existencias',
              'type':'number',
            }),
            label="Cantidad de piezas o equipos")
    class Meta:
      model = Bodega
      fields=['nombre_pieza','descripcion_pieza','serie_pieza','cantidad_pieza']

