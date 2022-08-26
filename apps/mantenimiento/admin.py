from django.contrib import admin
from .models import Mantenimiento
from django.contrib.auth.models import User
# Register your models here.


@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    autocomplete_fields = ['cliente','usuario']
    list_display = ('codigo_man','tipo_man','cliente','usuario',)

class UsuarioAdmin(User):
    search_fields = ['first_name', 'last_name' ]

    