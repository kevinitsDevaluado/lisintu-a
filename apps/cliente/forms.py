from apps.cliente.models import Cliente
from django import forms

#-------------- Formulario para el registro de clientes ----------------
#-----------------------------------------------------------------------
class ClienteForm(forms.ModelForm):
    nombre1_cliente = forms.CharField(
        max_length = 80,
        required=True,
        label='Primer Nombre',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control text-uppercase',
                'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()",
                'pattern':'[A-Za-záéíóú:, ,]+', 
                'onkeydown':"return /[A-Za-záéíóú, ,]/i.test(event.key)",
            }
        )
    )

    nombre2_cliente = forms.CharField(
        max_length = 80,
        required=True,
        label='Segundo Nombre',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control text-uppercase',
                'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()",
                'pattern':'[A-Za-záéíóú:, ,]+', 
                'onkeydown':"return /[A-Za-záéíóú, ,]/i.test(event.key)",
            }
        )
    )

    apellido1_cliente = forms.CharField(
        max_length = 80,
        required=True,
        label='Primer Apellido',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control text-uppercase',
                'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()",
                'pattern':'[A-Za-záéíóú:, ,]+', 
                'onkeydown':"return /[A-Za-záéíóú, ,]/i.test(event.key)",
            }
        )
    )

    apellido2_cliente = forms.CharField(
        max_length = 80,
        required=True,
        label='Segundo Apellido text-uppercase',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'onkeyup':"document.getElementById(this.id).value=document.getElementById(this.id).value.toUpperCase()",
                'pattern':'[A-Za-záéíóú:, ,]+', 
                'onkeydown':"return /[A-Za-záéíóú, ,]/i.test(event.key)",
            }
        )
    )

    cedula_cliente = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'oninput':"this.value = this.value.replace(/[^0-9]/g, '').replace(/(\..*?)\..*/g, '$1');",
                }),
                label='Cédula')

    telefono_cliente = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={
                'type':'phone',
                'class': 'form-control',
                'oninput':"this.value = this.value.replace(/[^0-9-]/g, '').replace(/(\..*?)\..*/g, '$1');",
                }),
                label='Teléfono de contacto')

    direccion_cliente = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control text-capitalize', 
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+'
                }),
                label='Dirección de contacto')

    email_cliente = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'type':'email',
                'class':'form-control'
                }),
                label='Correo Electrónico')

    class Meta:
        model = Cliente
        fields = ['nombre1_cliente', 'nombre2_cliente', 'apellido1_cliente', 'apellido2_cliente', 'cedula_cliente', 'telefono_cliente', 'direccion_cliente', 'email_cliente']