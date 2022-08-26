from django.urls import path, include
from .import views
from .views import bodega_ingreso , Bodega_Update, Bodega_Detail
urlpatterns = [
    path('bodega/',views.bodega_index, name='bodega_index'),
    #path('bodega_ingreso/',views.bodega_ingreso, name='bodega_ingreso'),
    path('bodega_consulta/',views.Bodega_Listado, name='bodega_consulta'),
    path('ingreso/', bodega_ingreso.as_view(), name='ingreso'),
    #path(r'^editar_bodega/(?P<pk>\d+)/$',Bodega_update.as_view(),name='editar_bodega'),
    path('bodega_update/<int:pk>',Bodega_Update.as_view(), name = 'bodega_update'),
    path('detalle_bodega/<int:pk>', Bodega_Detail.as_view(),name='detalle_bodega'),
    
]