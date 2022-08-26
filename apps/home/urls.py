from django.urls import path, include
from .import views

from .views import (
    pdf_reporte_cliente, pdf_reporte_tecnico,pdf_reporte_fichas,pdf_reporte_bodega,
)

urlpatterns = [
    path('',views.index_home, name='index'),
    path('contactenos/',views.contactenos, name='contactenos'),
    path('catalogos/',views.catalogos, name='catalogos'),
    path('consulta_cliente/',views.Consulta_Cliente, name='consulta_cliente'),
    path('dashboard_index/', views.index_dashboard, name='dashboard_index'),
    #----------------------- Busquedas ---------------------------------------
    path('busquedas_index/', views.Busquedas_index, name='busquedas_index'),
    path('busqueda_usuario/', views.Busqueda_Usuario, name='busqueda_usuario'),
    path('busqueda_cliente/', views.Busqueda_Cliente, name='busqueda_cliente'),
    path('busqueda_fichas/', views.Busqueda_Fichas, name='busqueda_fichas'),
    path('busqueda_bodega/',views.Busqueda_Bodega, name='busqueda_bodega'),
    #path('fake_email/', Pagina_email_send.as_view(), name='fake_email'),
    #----------------------- Reportes ------------------------------------------
    path('reportes_index/', views.Reporte_index, name='reportes_index'),
    path('reportes_clientes/', views.Reporte_Cliente, name='reportes_clientes'),
    path('reportes_tecnico/', views.Reporte_Tecnico, name='reportes_tecnico'),
    path('reportes_fichas/', views.Reporte_Fichas, name='reportes_fichas'),
    path('reportes_bodega/', views.Reporte_Bodega, name='reportes_bodega'),
    #----------------------- PDF - Reportes ------------------------------------
    path('pdf_reporte_cliente/<int:year>,<int:mes>', pdf_reporte_cliente.as_view(), name="pdf_reporte_cliente"),
    path('pdf_reporte_tecnico/<int:year>,<int:mes>,<int:id_tecnico>', pdf_reporte_tecnico.as_view(), name="pdf_reporte_tecnico"),
    path('pdf_reporte_ficha/<int:year>,<int:mes>', pdf_reporte_fichas.as_view(), name="pdf_reporte_ficha"),
    path('pdf_reporte_bodega/<int:year>,<int:mes>', pdf_reporte_bodega.as_view(), name="pdf_reporte_bodega"),
    #--------------------- PWA CPS ------------------------------------------------
    path('buscador_offline/',views.Buscador_offline, name='buscador_offline'),
    path('getdata/', views.getdata, name='getdata'),
]
