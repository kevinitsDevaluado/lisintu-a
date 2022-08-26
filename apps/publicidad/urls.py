from django.urls import path, include
from .import views
from .views import whatsapp2, urlIndex

urlpatterns = [
    path('publicidad_index/',views.publicidad_index, name='publicidad_index'),
    path('publicidad_correo/',views.enviar, name='publicidad_correo' ),
    path('publicidad_whastapp/',views.whatsapp, name='publicidad_whatsapp' ),
    path('detalle_mensaje/<int:pk>',whatsapp2.as_view(), name='detalle_mensaje'),
    path('actualizar_URL/',urlIndex.as_view(), name='actualizar_url'),
    #path('enviar_mensaje/',views.enviar2, name='enviar_mensaje' ),
    path('correo_ejemplo/',views.correo_ejemplo, name='correo_ejemplo'),
]