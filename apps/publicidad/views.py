from cgitb import text
from hashlib import new
from http import client
from importlib.resources import contents
from itertools import zip_longest
from multiprocessing import context
from pickle import FALSE, TRUE
from pipes import Template
from re import M
from typing import get_args
from django.db.models import Q
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.cliente.forms import Cliente
import webbrowser as web
import time
from django.views.generic import (CreateView, 
ListView, DetailView, 
UpdateView, TemplateView, 
DeleteView, View)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from email.mime.image import MIMEImage

from apps.publicidad.forms import mensaje_form, urlIndex_form



# Create your views here.
def correo_ejemplo(request):
    return render(request, 'dashboard/publicidad/correo.html')

def publicidad_index(request):
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    return render(request, 'dashboard/publicidad/publicidad_index.html', {'avatar': avatar,'nombre_apellido':nombre_apellido, 'info_personal': info_personal,})


def enviar(request):
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    model= Cliente
    cliente=[]
    for i in Cliente.objects.all():
        cliente.append(i.email_cliente)
        print(cliente)
    if request.method == "POST":
        #to = request.POST.get('toemail')
        to=cliente
        content = request.POST.get('content')
        content2= request.POST.get('content2')
        html_content = render_to_string('dashboard/publicidad/correo.html',{'title':'test email','content':content,'content2':content2})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            'Conoce Nuestras Ofertas',
            text_content,
            settings.EMAIL_HOST_USER,
            to
        )
        
        #email.attach_file(img)
        email.attach_alternative(html_content,'text/html')
        email.send()
        messages.success(request,'Se enviaron los mensajes con exito')

    return render(request,'dashboard/publicidad/publicidad_correo.html', {'cliente': cliente,'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido, 'title':'Enviar Correo'})


def whatsapp(request):
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    model= Cliente

    querySet = request.GET.get("buscar_cliente")
    if querySet:
        cliente = Cliente.objects.all().filter(
            Q(nombre1_cliente__icontains = querySet) |
            Q(nombre2_cliente__icontains = querySet) |
            Q(apellido1_cliente__icontains = querySet) |
            Q(apellido2_cliente__icontains = querySet) |
            Q(cedula_cliente__icontains = querySet)
            #Q(email_cliente__icontains = querySet)
        )
        usuario1 = Cliente.objects.filter(email_cliente = querySet)
        return render(request, 'dashboard/publicidad/publicidad_whatsapp.html', {'cliente': cliente, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})
    else:
        return render(request, 'dashboard/publicidad/publicidad_whatsapp.html', {'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})


class whatsapp2(SuccessMessageMixin, TemplateView ):
    template_name = 'dashboard/publicidad/enviar_mensaje.html'
    form_class = mensaje_form 

    def get_context_data(self, **kwargs):
        context = super(whatsapp2, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form']= self.form_class(self.request.GET)
        pk = self.kwargs.get('pk', 0)
        cliente = Cliente.objects.get(id = pk)
        #------------------------- Datos de Header ------------------------
        info_personal = self.request.user.first_name+' '+self.request.user.last_name
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #------------------------------------------------------------------
        context['cliente'] = cliente
        context['info_personal'] = info_personal
        context['avatar'] = avatar
        context['nombre_apellido'] = nombre_apellido
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        mensaje = self.request.POST.get('mensaje')
        num = self.request.POST.get('numero')
        context['new_variable'] = mensaje
        
        web.open('https://web.whatsapp.com/send?phone=593'+num+'&text='+mensaje)

        messages.success(request,'Se ha conectado con exito al contaccto del Cliente.')

        return self.render_to_response(context)


class urlIndex(SuccessMessageMixin, TemplateView):
    template_name = 'dashboard/publicidad/actualizar_url.html'
    form_class = urlIndex_form
    
    def get_context_data(self, **kwargs):
        context = super(urlIndex, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form']= self.form_class(self.request.GET)
        pk = self.kwargs.get('pk', 0)
        
        #------------------------- Datos de Header ------------------------
        info_personal = self.request.user.first_name+' '+self.request.user.last_name
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #------------------------------------------------------------------

        context['info_personal'] = info_personal
        context['avatar'] = avatar
        context['nombre_apellido'] = nombre_apellido
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        mensaje = self.request.POST.get('urlcontent')
        
        context['new_variable'] = mensaje
        if(mensaje !=''):
            messages.success(request,'Se ha actualizado la URL del catálogo con exito.')
        else:
            messages.warning(request,'El campo se encuentra vacio')
        return self.render_to_response(context)

