from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from apps.usuario.models import Perfil


#---------------------------------------- opciones para selecionar ---------------------------------------
areas_opciones = (('', 'Sin Datos'),('Ventas', 'Ventas'),('Soporte Técnico', 'Soporte Técnico'),('Administración', 'Administración'))
cargos_opciones = (('', 'Sin Datos'),('vendedor', 'Vendedor'),('Técnico-PC', 'Técnico-PC'),('Técnico-AUD', 'Técnico-AUD'),('Administración', 'Administración'))
#---------------------------------------------------------------------------------------------------------


#-------------- Formulario para la edicion de datos del personal ----------------
#---------------------------como administrador ----------------------------------

class UpdateUserForm(forms.ModelForm):

    username = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-záéíóú:, ,--,@,_,[0-9]+',
                'placeholder':'Nombre de Usuario',
                'type':'text',
                'title':"El nombre de usuario no debe contener caracteres especiales u otros solo numeros y letras"
                }),
                label='Nombre de usuario')

    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-záéíóú:, ,]+', 
                'onkeydown':"return /[A-Za-záéíóú, ,]/i.test(event.key)",
                'placeholder':'Nombres',
                'type':'text',
                }),
                label='Nombres')

    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-záéíóú:, ,]+', 
                'onkeydown':"return /[A-Za-záéíóú, ,]/i.test(event.key)",
                'placeholder':'Nombres',
                'type':'text',
                }),
                label='Nombres')

    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'Correo Electrónico',
                'type':'email',
                }),
                label='Nombres')

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget = forms.CheckboxSelectMultiple
        )

    class Meta:
        model = User
        fields = {'username','first_name','last_name','email','groups','is_staff'}

#------------------------------------------------------------------------------------------

class UpdatePerfilForm(forms.ModelForm):
    cedula_perfil = forms.CharField(
        max_length=10,
        min_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'oninput':"this.value = this.value.replace(/[^0-9]/g, '').replace(/(\..*?)\..*/g, '$1');",
                }),
                label='Cédula')

    direccion_perfil = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+'
                }),
                label='Dirección de contacto')

    telefono_perfil = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={
                'type':'phone',
                'class': 'form-control',
                'oninput':"this.value = this.value.replace(/[^0-9-]/g, '').replace(/(\..*?)\..*/g, '$1');",
                }),
                label='Teléfono de contacto')

    area_perfil = forms.ChoiceField(
        choices=areas_opciones,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
                }),
                label='Area de Trabajo')
    
    cargo_perfil = forms.ChoiceField(
        choices=cargos_opciones, 
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
                }),
                label='Cargo que ocupa')
                
    '''cargo_perfil = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_]+'}),
                label='Cargo que ocupa')'''
    
    class Meta:
        model = Perfil
        fields = ['cedula_perfil','direccion_perfil','telefono_perfil','area_perfil','cargo_perfil',]

#================================================================================
#-------------- Formulario para el registro de un nuevo trabajador --------------
#---------------------------como administrador ----------------------------------
#================================================================================

class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control'
        })

    username = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-záéíóú:, ,--,@,_,[0-9]+',
                'placeholder':'Nombre de Usuario',
                'type':'text',
                'title':"El nombre de usuario no debe contener caracteres especiales u otros solo numeros y letras"
                }),
                label='Nombre de usuario')

    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-záéíóú:, ,]+', 
                'onkeydown':"return /[A-Za-záéíóú, ,]/i.test(event.key)",
                'placeholder':'Nombres',
                'type':'text',
                }),
                label='Nombres')
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-záéíóú:, ,]+', 
                'onkeydown':"return /[A-Za-záéíóú, ,]/i.test(event.key)",
                'placeholder':'Apellidos',
                'type':'text',
                }),
                label='Nombres')

    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'Correo Electrónico',
                'type':'email',
                }),
                label='Nombres')
    
    password1 = forms.PasswordInput(
        attrs={
            'class':'form-control'})

    password2 = forms.PasswordInput(
        attrs={
            'class':'form-control'})
    
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget = forms.CheckboxSelectMultiple
        )

    class Meta:
        model = User
        model._meta.get_field('email')._unique = True
        model._meta.get_field('username')._unique = True
        fields = {'username','first_name','last_name','email','password1','password2','groups','is_staff'}
    '''
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'Ya existe un usuario con el email.'
            self.add_error('email', msg)           
    
        return self.cleaned_data
    '''
#------------------------------------------------------------------------------------------

class PerfilForm(forms.ModelForm):
    cedula_perfil = forms.CharField(
        max_length=10,
        min_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'oninput':"this.value = this.value.replace(/[^0-9]/g, '').replace(/(\..*?)\..*/g, '$1');",
                'placeholder':'Cédula',
                }),
                label='Cédula')

    direccion_perfil = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'pattern':'[A-Za-z0-9áéíóú:, ,--,@,_,[0-9]+',
                'placeholder':'Dirección',
                }),
                label='Dirección de contacto')

    telefono_perfil = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={
                'type':'phone',
                'class': 'form-control',
                'oninput':"this.value = this.value.replace(/[^0-9-]/g, '').replace(/(\..*?)\..*/g, '$1');",
                'placeholder':'Teléfono',
                }),
                label='Teléfono de contacto')

    area_perfil = forms.ChoiceField(
        choices=areas_opciones,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
                }),
                label='Area de Trabajo')
    
    cargo_perfil = forms.ChoiceField(
        choices=cargos_opciones, 
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
                }),
                label='Cargo que ocupa')
                
    class Meta:
        model = Perfil
        fields = ['cedula_perfil','direccion_perfil','telefono_perfil','area_perfil','cargo_perfil',]