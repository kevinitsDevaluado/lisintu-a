import email
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#---------------------------------------- opciones para selecionar ---------------------------------------
areas_opciones = (('Ventas', 'Ventas'),('Soporte Técnico', 'Soporte Técnico'),('Administración', 'Administración'))
cargos_opciones = (('vendedor', 'Vendedor'),('Técnico-PC', 'Técnico-PC'),('Técnico-AUD', 'Técnico-AUD'),('Administración', 'Administración'))
#---------------------------------------------------------------------------------------------------------

class Perfil(models.Model):
    cedula_perfil= models.CharField(max_length=10, blank=True, unique=True)
    telefono_perfil= models.CharField(max_length=10, blank=True)
    direccion_perfil= models.CharField(max_length=80, blank=True)
    area_perfil= models.CharField(max_length=80, blank=True)
    cargo_perfil= models.CharField(max_length=80, blank=True)
    # ForenKeys  --> relacion con auth_user
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
            return ' {} {} {} {}' .format(self.usuario.first_name, self.usuario.last_name, '/', self.cargo_perfil)


def get_first_name(self):
    return ' {} {} {}' .format(self.first_name, self.last_name, self.email)

User.add_to_class("__str__", get_first_name)
