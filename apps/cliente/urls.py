from django.urls import path
from .import views
from .views import Cliente_Registrar, Cliente_Detail, Cliente_Update

urlpatterns = [
    path('cliente_index/',views.cliente_index, name='cliente_index'),
    path('listado_clientes/', views.Cliente_Listado, name='listado_clientes'),
    path('registro_cliente/',Cliente_Registrar.as_view(), name='registrar_cliente'),
    path('detalle_cliente/<int:pk>',Cliente_Detail.as_view(), name='detalle_cliente'),
    path('editar_cliente/<int:pk>,<int:admin_pk>', Cliente_Update.as_view(), name='editar_clientes'),
]