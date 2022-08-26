from django.urls import path
from .import views
from .views import (
    Ficha_Detalle_2, Mantenimiento_listado, Ficha_Registrar, Ficha_Detalle, 
    Ficha_Editar, Ficha_Gestionar, Mantenimientos_Asignados,
    Mantenimientos_Historial, Mantenimientos_Proceso, Ficha_Finalizar, Ficha_Entregar,ViewPDF_Ficha)

urlpatterns = [
    path('mantenimiento_index/',views.mantenimiento_index, name='mantenimiento_index'),
    #------------------------------------------------------------------------------------------
    path('mantenimiento_listado/', Mantenimiento_listado.as_view(), name='mantenimiento_listado'),
    path('mantenimiento_registrar/', Ficha_Registrar.as_view(), name='mantenimiento_registrar'),
    path('mantenimiento_detalle/<int:pk>',Ficha_Detalle.as_view(), name='mantenimiento_detalle'),
    path('ficha_detalle/<int:pk>',Ficha_Detalle_2.as_view(), name='ficha_detalle'),
    path('mantenimiento_editar/<int:pk>',Ficha_Editar.as_view(), name='mantenimiento_editar'),
    #--------------------------- Gestion de Fichas ---------------------------------------------
    path('ficha_gestionar/<int:pk>',Ficha_Gestionar.as_view(), name='ficha_gestionar'),
    path('ficha_finalizar/<int:pk>',Ficha_Finalizar.as_view(), name='ficha_finalizar'),
    path('ficha_entregar/<int:pk>',Ficha_Entregar.as_view(), name='ficha_entregar'), #ventas
    #-------------------------------- Mantenimientos Tecnicos ----------------------------------
    path('mantenimiento_asignado/', Mantenimientos_Asignados.as_view(), name='mantenimiento_asignado'),
    path('mantenimiento_historial/', Mantenimientos_Historial.as_view(), name='mantenimiento_historial'),
    path('mantenimiento_proceso/', Mantenimientos_Proceso.as_view(), name='mantenimiento_proceso'),
    #----------------------- Generar PDF ficha -------------------------------------
    path('pdf_ficha/<int:pk>', ViewPDF_Ficha.as_view(), name="pdf_ficha"),
    #----------------------- Pruebas de estilo
    path('audiovisual_mant_index/',views.audiovisual_mant_index, name='audiovisual_mant_index'),
    path('tecnologia_mant_index/',views.tecnologia_mant_index, name='tecnologia_mant_index'),
    path('correo_prueba/',views.correo_prueba, name='correo_prueba'),
    path('pdf_prueba/',views.ficha_pdf_prueba, name='pdf_prueba'),
]