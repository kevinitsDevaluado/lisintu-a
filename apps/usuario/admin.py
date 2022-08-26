from django.contrib import admin
from .models import Perfil
# Register your models here.


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    search_fields = ['cargo_perfil','usuario__first_name']
    list_display = (
        'usuario', 
        'cedula_perfil', 
        'telefono_perfil', 
        'area_perfil', 
        'cargo_perfil',
        )

