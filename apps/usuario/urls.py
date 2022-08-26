from django.urls import path
from .import views
from .views import Usuario_Listado_funcion,Usuario_Detail,Usuario_Delete,Usuario_Update,SignUpView 

urlpatterns = [
    path('usuario_index/',views.usuario_index, name='usuario_index'),
    path('listado_usuarios/', Usuario_Listado_funcion, name='listado_usuarios'),
    path('perfil_usuario/<int:pk>', Usuario_Detail.as_view(), name='perfil_usuarios'),
    path('eliminar/<int:pk>', Usuario_Delete.as_view(), name='eliminar_usuarios'),
    path('editar_usuario/<int:pk>,<int:admin_pk>', Usuario_Update.as_view(), name='editar_usuarios'),
    path('signup/', SignUpView.as_view(), name='signup'),
]