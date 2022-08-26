from django.db import models
from django.contrib.auth.models import User
from apps.cliente.models import Cliente
from apps.usuario.models import Perfil
# Create your models here.

estados_soli = (('Ingresado','Ingresado'),('En Proceso','En Proceso'),('Finalizado','Finalizado'),('Entregado','Entregado'))
tipo_mante2 = (('Tecnologico','Tecnologico'),('Audiovisual','Audiovisual'))
tipo_mante = (('Soporte Técnico','Soporte Técnico'),('Soporte Técnico','Soporte Técnico'))
class Mantenimiento(models.Model):
    codigo_man = models.CharField(max_length=100, blank=True, verbose_name="Código de Mantenimiento")
    tipo_man =  models.CharField(max_length = 200, choices=tipo_mante, blank = True, verbose_name="Tipo de Mantenimiento")
    estado_man = models.CharField(max_length = 200, default='Ingresado', choices=estados_soli, verbose_name='Estado de Mantenimiento')
    fecha_ingreso_man = models.DateTimeField(auto_now_add = True, verbose_name='Fecha de Ingreso')
    fecha_salida_man = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Salida')
    fecha_entrega_man = models.DateTimeField(null=True,blank=True, verbose_name='Fecha de Entrega')
    #--------------------------- datos del equipo ------------------------------------------
    tipo_equipo_man =  models.CharField(max_length = 100, blank = True, verbose_name="Tipo de Equipo")
    marca_equipo_man = models.CharField(max_length=100, blank=True, verbose_name="Marca del Equipo")
    modelo_equipo_man = models.CharField(max_length=100, blank=True, verbose_name="Modelo del Equipo")
    accesorios_equipo_man = models.TextField(blank=True, verbose_name='Accesorios del equipo')
    falla_equipo_man = models.TextField(blank=True, verbose_name='Fallas del equipo')
    #--------------------------- Informacion del Tecnico ------------------------------------
    procedimiento_man = models.TextField(blank=True, verbose_name='Procedimiento Realizado')
    observaciones_man = models.TextField(blank=True, verbose_name='Oservaciones del Tecnico')
    costo_man = models.FloatField(null=True, blank=True, verbose_name="Costo del Mantenimiento")
    #--------------------------- Relaciones a tablas de cliente y Tecnicos ------------------
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True)
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE, blank=True)

    



