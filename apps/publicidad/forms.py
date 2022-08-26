from dataclasses import fields
import numbers
from django import forms

class mensaje_form(forms. Form):
    
    mensaje = forms.CharField(
        max_length = 80,
        required=True,
        label='Primer Nombre',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()",
                #'pattern':'[A-Za-záéíóú:, ,]+', 
                #'onkeydown':"return /[A-Za-záéíóú, ,]/i.test(event.key)",
            }
        )
    )

class urlIndex_form(forms.Form):
    url = forms.URLField(
        required= True,
    )