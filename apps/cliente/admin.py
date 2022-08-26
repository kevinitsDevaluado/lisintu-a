from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields = ['cedula_cliente','nombre1_cliente','nombre2_cliente','apellido1_cliente','apellido2_cliente' ]
    list_display = (
        'id',
        'nombre1_cliente',
        'apellido1_cliente',
        'cedula_cliente',
        'email_cliente'
    )