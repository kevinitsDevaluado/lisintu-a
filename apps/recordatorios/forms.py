from dataclasses import fields
import numbers
from django import forms

from apps.recordatorios.models import Recordatorios



class Recordatorios_form(forms.ModelForm):
    fecha_rec = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()", 
                'type':'date',
            }
        )
    )
    descripcion_rec = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
            'class': 'form-control',
                'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()", 
                'pattern':'[A-Za-záéíóú:, ,]+', 
                'onkeydown':"return /[A-Za-záéíóú, ,]/i.test(event.key)",
                'placeholder':'Ingrese una pequeña descripción del equipo o pieza',
                'type':'text',
                'rows':'4',
            }),
            label="Descripción")
    class Meta:
        model = Recordatorios
        fields=['fecha_rec','descripcion_rec']