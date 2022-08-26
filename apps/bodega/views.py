from datetime import datetime
from multiprocessing import context
from pickle import FALSE
from django.shortcuts import render, HttpResponseRedirect,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from apps.bodega.forms import Bodega_form
from django.views.generic import (CreateView, 
ListView, DetailView, 
UpdateView, TemplateView, 
DeleteView, View)
from django.contrib.auth.models import User
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.bodega.models import Bodega
from apps.usuario.models import Perfil
from django.forms import ModelForm

# Create your views here.

def bodega_index(request):
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    
    return render(request, 'dashboard/bodega/bodega_index.html', {'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})
#----------------------------------listado de elementos de bodega---------------------------------------------------
@login_required
def Bodega_Listado(request):
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    bodega = Bodega.objects.all()
    return render(request,'dashboard/bodega/bodega_consulta.html',{'bodega':bodega,'avatar': avatar,'nombre_apellido':nombre_apellido})

    
    
@login_required
def Usuario_Listado_funcion(request):
    #----- Informacion User Logeado ----
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    #----- Informacion User Logeado ----
    usuario = User.objects.all()
    return render(request, 'dashboard/usuario/usuario_listado.html',{
        'usuario':usuario,
        'avatar': avatar, 
        'nombre_apellido':nombre_apellido
        })

    

#----------------------------------Ingreso de elementos en bodega----------------------------------------------------
@method_decorator(login_required, name='dispatch')
class bodega_ingreso(CreateView):
    model = Bodega
    form_class = Bodega_form
    template_name = 'dashboard/bodega/bodega_ingreso.html'
    success_url = reverse_lazy('bodega_index')

    def get_context_data(self, **kwargs): 
        
        context = super(bodega_ingreso, self).get_context_data(**kwargs)
    
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        context['avatar'] = avatar
        context['nombre_apellido'] = nombre_apellido
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Se ha registrado en bodega correctamente ")
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(request,"Existio un problema con tus campos revisalos")
            return self.render_to_response(self.get_context_data(form=form))
#------------------------------------Editar elementos de la bodega------------------------------------------------------------


    
@login_required
def Usuario_Listado_funcion(request):
    #----- Informacion User Logeado ----
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    #----- Informacion User Logeado ----
    usuario = User.objects.all()
    return render(request, 'dashboard/usuario/usuario_listado.html',{
        'usuario':usuario,
        'avatar': avatar, 
        'nombre_apellido':nombre_apellido
        })


@method_decorator(login_required, name='dispatch')
class Bodega_Detail(SuccessMessageMixin, TemplateView):
    template_name = 'dashboard/bodega/bodega_detalle.html'
    def get_context_data(self, **kwargs):
        context = super(Bodega_Detail, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        bodega = Bodega.objects.get(id=pk)
        #----- Informacion User Logeado ----
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #----- Fin Informacion User Logeado ----
        return {'bodega': bodega, 'avatar': avatar, 'nombre_apellido':nombre_apellido}

@method_decorator(login_required, name='dispatch')
class Bodega_Update(SuccessMessageMixin, UpdateView):
    model = Bodega
    form_class = Bodega_form
    template_name = 'dashboard/bodega/bodega_editar.html'

    def get_context_data(self, **kwargs):
        context = super(Bodega_Update, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        bodega = self.model.objects.get(id = pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance = bodega)
        context['id']= pk
        print(bodega)

        cliente = self.model.objects.get(id = pk)
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        context['cliente'] = cliente
        context['avatar'] = avatar
        context['nombre_apellido'] = nombre_apellido
        context['bodega'] = bodega
        messages.warning(self.request,"Revisa todos los datos antes de actualizar.")
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_bodega = kwargs['pk']

        bodegaPK = self.model.objects.get(id = id_bodega)
        print(bodegaPK)
        form = self.form_class(request.POST,instance = bodegaPK)

        if form.is_valid():
            form.save()
            messages.success(request,"Se ha registrado en bodega correctamente ")
            return HttpResponseRedirect(reverse_lazy('bodega_index'))
        else:
            messages.error(request,"Existio un problema con tus campos revisalos")
            return HttpResponseRedirect(reverse_lazy('bodega_index'))