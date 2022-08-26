from django.db import models

# Create your models here.

class Cliente(models.Model):
    nombre1_cliente = models.CharField(max_length=100, blank=True, verbose_name="Primer Nombre")
    nombre2_cliente = models.CharField(max_length=100, blank=True, verbose_name="Segundo Nombre")
    apellido1_cliente = models.CharField(max_length=100, blank=True, verbose_name="Primer Apellido")
    apellido2_cliente = models.CharField(max_length=100, blank=True, verbose_name="Segundo Apellido")
    cedula_cliente= models.CharField(max_length=10, blank=True, verbose_name="Cédula", unique=True)
    telefono_cliente= models.CharField(max_length=10, blank=True, verbose_name="teléfono")
    direccion_cliente= models.CharField(max_length=80, blank=True, verbose_name="Dirección")
    email_cliente = models.EmailField(verbose_name="Correo Electronico")

    def __str__(self):
        return ' {} {} {} {} {} {}' .format(self.cedula_cliente, '  ->  ' ,self.nombre1_cliente, self.nombre2_cliente, self.apellido1_cliente,  self.apellido2_cliente)