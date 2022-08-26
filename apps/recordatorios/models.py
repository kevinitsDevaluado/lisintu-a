from django.db import models

# Create your models here.
class Recordatorios(models.Model):
    descripcion_rec=models.CharField(max_length=200,blank=False)
    fecha_rec=models.DateField()