"""proyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# -------------- Configuracion estetica del Admin ------------
admin.site.site_header = 'Gestion de Servicios - CPS'
admin.site.site_title = 'ADMINISTRACIÓN'
#admin.site.site_url = 'http://coffeehouse.com/'
admin.site.index_title = 'ADMINISTRACIÓN'
admin.empty_value_display = '**Empty**'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls')),
    # Direcciones para apps
    path('usuario/',  include('apps.usuario.urls')),
    path('cliente/',  include('apps.cliente.urls')),
    path('mantenimiento/',  include('apps.mantenimiento.urls')),
    path('bodega/', include('apps.bodega.urls')),
    path('publicidad/', include('apps.publicidad.urls')),
    path('recordatorios/',include('apps.recordatorios.urls')),
    # Control de Secciones
    path('accounts/', include('django.contrib.auth.urls')), # Login control
    # Para PWA
    path('',include('pwa.urls')), # Para parte de service worked
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

