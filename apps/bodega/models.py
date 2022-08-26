from django.db import models
# Create your models here.
class Bodega(models.Model):
    nombre_pieza=models.CharField(max_length=100, blank=True)
    serie_pieza=models.CharField(max_length=30,blank=True)
    descripcion_pieza=models.CharField(max_length=300, blank=True)
    cantidad_pieza=models.IntegerField(blank=True)
    fecha_pieza=models.DateField(auto_now_add=True)

