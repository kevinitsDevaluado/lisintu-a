from django.urls import path, include
from .import views
from .views import Recordatorio_Delete, recordatorios_ingreso
urlpatterns = [
    path('recordatorios/',views.recordatorios_index, name='recordatorios_index'),
    path('recordatorios_ingreso/',recordatorios_ingreso.as_view(), name='recordatorios_ingreso'),
    path('recordatorios_consulta/',views.Recordatorios_Listado, name='recordatorios_consulta'),
    path('eliminar/<int:pk>', Recordatorio_Delete.as_view(), name='eliminar_recordatorio'),

]