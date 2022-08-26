from datetime import datetime
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
#todo------------------ Para autenticar usuarios ---------------------
from django.contrib.auth import login, authenticate
#todo ----------------- Para Vistas basadas en Clases ----------------
from django.views import generic
from django.views.generic import (CreateView, 
ListView, DetailView, 
UpdateView, TemplateView, 
DeleteView, View)
#todo ----------------- Para Mesnsajes en pantalla --------------
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
#todo ----------------- Llamada Formularios ----------------------
from apps.cliente.forms import ClienteForm
from apps.mantenimiento.forms import (
    Ficha_Registrar_Form, Ficha_Editar_Form, 
    Ficha_Gestion_Form, Ficha_Finalizar_Form, Ficha_Entrega_Form)
#todo ----------------- Para seguridad URLS ----------------------
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
#todo ----------------- Para Generar y Enviar Correo -------------
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
#todo ----------------- Importar modelos de las apps -------------
from django.contrib.auth.models import User
from apps.usuario.models import Perfil
from apps.cliente.models import Cliente
from apps.mantenimiento.models import Mantenimiento
#todo---------------- Para renderizar a pdf ------------------
from io import BytesIO
from django.views import View
from xhtml2pdf import pisa





#todo====================================================================================================
#todo ------------------ funcion para generar codigo de busqueda de ficha -------------------
#todo====================================================================================================

def Generar_codigo():
    import string
    import random
    length_of_string = 10
    codigo1 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
    return codigo1


#todo====================================================================================================
#todo--------------------------- Funciones para pagina principal ----------------------------
#todo----------------------------------- Mantenimientos -------------------------------------
#todo====================================================================================================

@login_required
def mantenimiento_index(request):
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    
    return render(request, 'dashboard/mantenimiento/mantenimiento_index.html', {'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})

@login_required
def tecnologia_mant_index(request):
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    
    return render(request, 'dashboard/mantenimiento/tecnologia/tecnologia_index.html', {'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})

@login_required
def audiovisual_mant_index(request):
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    
    return render(request, 'dashboard/mantenimiento/audiovisual/audiovisual_index.html', {'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})


#todo====================================================================================================
#todo--------------------------- Listado de mantenimientos ----------------------------
#todo====================================================================================================

@method_decorator(login_required, name='dispatch')
class Mantenimiento_listado(SuccessMessageMixin, TemplateView):
    template_name = 'dashboard/mantenimiento/mantenimiento_listado.html'
    model = Mantenimiento
    
    def get_context_data(self, *args, **kwargs):
        #------------------------- Datos de Header ------------------------
        info_personal = self.request.user.first_name+' '+self.request.user.last_name
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #------------------------------------------------------------------
        fichas = Mantenimiento.objects.all().order_by('-fecha_ingreso_man')
        return {
            'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido,
            'fichas':fichas,
            }


#todo====================================================================================================
#todo--------------------------- Generar Ficha de Mantenimientos ----------------------------
#todo====================================================================================================

#!--- Falta proceso de notificacion para correo o whatsapp / generar pdf
@method_decorator(login_required, name='dispatch')
class Ficha_Registrar(SuccessMessageMixin, CreateView):
    model = Mantenimiento
    form_class = Ficha_Registrar_Form
    template_name = 'dashboard/mantenimiento/mantenimiento_registrar.html'
    success_message = 'Se ha generado correctamente la ficha de mantenimiento con copia al Cliente'

    def get_context_data(self, **kwargs):
        context = super(Ficha_Registrar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
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
        self.object = self.get_object
        form = self.form_class(request.POST)
        codigo_ficha = Generar_codigo()
        if form.is_valid():

            new = form.save(commit=False)
            new.codigo_man = codigo_ficha
            new.save()
            pk_ficha=new.id

            #?----------- envio del detalle al cliente correo ------------
            ficha_datos = Mantenimiento.objects.get(id = pk_ficha)
            Send_Email_Entrega(ficha_datos)
            #?------------------------------------------------------------
            messages.success(request, self.success_message)
            return HttpResponseRedirect(reverse_lazy('mantenimiento_listado'))
            #return self.render_to_response(self.get_context_data(form=form))
        else:
            #print(form.errors)
            messages.error(request,"Existio un problema con tus campos revisalos")
            return self.render_to_response(self.get_context_data(form=form))


#todo====================================================================================================
#todo--------------------------- Detalle de las Fichas ----------------------------
#todo====================================================================================================

@method_decorator(login_required, name='dispatch')
class Ficha_Detalle_2(SuccessMessageMixin, TemplateView):
    template_name = 'dashboard/mantenimiento/ficha_detalle.html'
    def get_context_data(self, *args, **kwargs):
        context = super(Ficha_Detalle_2, self).get_context_data(**kwargs)
        #------------------------- Datos de Header ------------------------
        info_personal = self.request.user.first_name+' '+self.request.user.last_name
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #------------------------------------------------------------------
        #------------------------- Consulta de la ficha -------------------
        pk_ficha = self.kwargs.get('pk', 0)
        ficha = Mantenimiento.objects.get(id = pk_ficha)
        return {'ficha':ficha, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido}


@method_decorator(login_required, name='dispatch')
class Ficha_Detalle(SuccessMessageMixin, TemplateView):
    template_name = 'dashboard/mantenimiento/mantenimiento_detalle.html'
    def get_context_data(self, *args, **kwargs):
        context = super(Ficha_Detalle, self).get_context_data(**kwargs)
        #------------------------- Datos de Header ------------------------
        info_personal = self.request.user.first_name+' '+self.request.user.last_name
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #------------------------------------------------------------------
        #------------------------- Consulta de la ficha -------------------
        pk_ficha = self.kwargs.get('pk', 0)
        ficha = Mantenimiento.objects.get(id = pk_ficha)
        #return {'ficha':ficha, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido}
        #------------------------------------------------------------------
        context['info_personal'] = info_personal
        context['avatar'] = avatar
        context['nombre_apellido'] = nombre_apellido
        context['ficha'] = ficha
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        ficha = context['ficha']
        print(ficha.id)

        #--------- update para poner en proceso el mantenimiento ------------------
        estado_ficha = Mantenimiento.objects.filter(id=ficha.id).update(estado_man ='En Proceso')
        messages.success(request,"Se ha puesto en marcha correctamente el mantenimiento.")
        #--------------------------------------------------------------------------
        return HttpResponseRedirect(reverse_lazy('mantenimiento_detalle', kwargs=kwargs ))




#todo====================================================================================================
#todo-------------------------------------- Edicion de Ficha --------------------------------------------
#todo====================================================================================================

@method_decorator(login_required, name='dispatch')
class Ficha_Editar(SuccessMessageMixin, UpdateView):
    model = Mantenimiento
    template_name = 'dashboard/mantenimiento/mantenimiento_editar.html'
    form_class = Ficha_Editar_Form

    def get_context_data(self,**kwargs):
        context = super(Ficha_Editar, self).get_context_data(**kwargs)
        pk_ficha_editar = self.kwargs.get('pk', 0)
        ficha_editar = self.model.objects.get(id = pk_ficha_editar)
        if 'form' not in context:
            context['form'] = self.form_class(instance =ficha_editar)
        #------------------------- Datos de Header ------------------------
        info_personal = self.request.user.first_name+' '+self.request.user.last_name
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #------------------------------------------------------------------
        context['info_personal'] = info_personal
        context['avatar'] = avatar
        context['nombre_apellido'] = nombre_apellido
        context['ficha'] = ficha_editar
        context['id'] = pk_ficha_editar
        messages.warning(self.request,"Presta mucha atención con los cambios que realices en este apartado.")
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_ficha = kwargs['pk']
        ficha_datos = self.model.objects.get(id = id_ficha)
        form = self.form_class(request.POST, instance = ficha_datos)
        if form.is_valid():
            estado_ficha = form.cleaned_data['estado_man']
            '''
            if estado_ficha == ficha_datos.estado_man:
                messages.info(request,"No se realizaron cambios en la Ficha.")
                return HttpResponseRedirect(reverse_lazy('mantenimiento_detalle', kwargs=kwargs ))
            else:
                new = form.save(commit=False)
                form.save()
                messages.success(request,"Se ha modificado los datos del la Ficha correctamente.")
                return HttpResponseRedirect(reverse_lazy('mantenimiento_detalle', kwargs=kwargs ))
            '''
            new = form.save(commit=False)
            form.save()
            messages.success(request,"Se han modificado los datos del la Ficha correctamente.")
            return HttpResponseRedirect(reverse_lazy('mantenimiento_detalle', kwargs=kwargs ))
        else:
            messages.error(request,"Existio un problema con tus campos revisalos antes de Guardarlos.")
            return self.render_to_response(self.get_context_data(form=form))


#todo====================================================================================================
#todo--------------------------------- Gestionar Esatdo de Ficha ----------------------------------------
#todo====================================================================================================
#todo----- Se cambia el estado del mantenimiento a otra fase --------------------------------------------
#todo----- Si estado cambia a Finalizado se genera la fecha en la cual se finalizo el mantenimiento -----
#todo----- Si estado cambia a entregado se genera la fecha en la cual se entrego el equipo al cliente ---
#todo----------------------------------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class Ficha_Gestionar(SuccessMessageMixin, UpdateView):
    model = Mantenimiento
    template_name = 'dashboard/mantenimiento/gestion_fichas/admin/gestion_fichas.html'
    form_class = Ficha_Gestion_Form

    def get_context_data(self,**kwargs):
        context = super(Ficha_Gestionar, self).get_context_data(**kwargs)
        pk_ficha_editar = self.kwargs.get('pk', 0)
        ficha_editar = self.model.objects.get(id = pk_ficha_editar)
        if 'form' not in context:
            context['form'] = self.form_class(instance =ficha_editar)
        #------------------------- Datos de Header ------------------------
        info_personal = self.request.user.first_name+' '+self.request.user.last_name
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #------------------------------------------------------------------
        context['info_personal'] = info_personal
        context['avatar'] = avatar
        context['nombre_apellido'] = nombre_apellido
        context['ficha'] = ficha_editar
        context['id'] = pk_ficha_editar
        messages.warning(self.request,"Presta mucha atención con los cambios que realices en este apartado.")
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_ficha = kwargs['pk']
        ficha_datos = self.model.objects.get(id = id_ficha)
        estado_ficha_bdd = ficha_datos.estado_man
        form = self.form_class(request.POST, instance = ficha_datos)

        if form.is_valid():

            estado_ficha = form.cleaned_data['estado_man']
            
            if estado_ficha == estado_ficha_bdd:
                #---- Cuando no hay cambios en el estado de la ficha ----
                messages.info(request,"No se realizaron cambios en la Ficha.")
                return HttpResponseRedirect(reverse_lazy('mantenimiento_detalle', kwargs=kwargs ))
            else:
                #---- Cuando el estado cambia a En Proceso
                if estado_ficha == 'En Proceso':
                    #?----------- Procesos en estado En Proceso -----------
                    '''
                    1) se notifica que el mantenimiento esta en proceso
                    '''
                    fecha_salida = datetime.now()
                    new_ficha = form.save(commit=False)
                    new_ficha.fecha_salida_man = fecha_salida
                    new_ficha.estado_man ='En Proceso'
                    form.save()

                    #!---------- 1 ---------- falta desarollar

                    messages.success(request,"Se ha cambiado a - En Proceso - el estado de la ficha.")
                    return HttpResponseRedirect(reverse_lazy('mantenimiento_detalle', kwargs=kwargs ))
                #---- Cuando el estado cambia a Finalizado
                elif estado_ficha == 'Finalizado':
                    #?----------- Procesos en estado de Finalizado -----------
                    '''
                    1) se habilita los campos de Procedimiento y observaciones
                    2) se obtiene los datos de Procedimiento y observaciones (x)
                    3) se obtiene la fecha y hora en la que se finaliza el mantenimiento (x)
                    4) se almacena en la BDD los datos obtenidos ( fecha, Procedimiento y observaciones ) (x)
                    5) se notifica que el mantenimiento finalizo
                    '''
                    costo_man = form.cleaned_data['costo_man']
                    fecha_salida = datetime.now()
                    #?---------- 4 ---------- 
                    new_ficha = form.save(commit=False)
                    new_ficha.fecha_salida_man = fecha_salida
                    new_ficha.costo_man = costo_man
                    new_ficha.estado_man ='Finalizado'
                    form.save()
                    #!---------- 1 - 5 ---------- falta desarollar

                    messages.success(request,"Se ha cambiado a - Finalizado - el estado de la ficha.")
                    return HttpResponseRedirect(reverse_lazy('mantenimiento_detalle', kwargs=kwargs ))
                #---- Cuando el estado cambia a Entregado
                elif estado_ficha == 'Entregado':
                    #?----------- Procesos en estado de entrega -----------
                    '''
                    1) se habilita el campo de precio en el formulario (x)
                    2) se obtiene los datos del precio del formulario (x)
                    3) se obtiene la fecha y hora en la que se le entrego al cliente el equipo (x)
                    4) se almacena en la BDD los datos obtenidos ( fecha y precio ) (x)
                    5) se envia copia de ficha entregada al dueño del equipo
                    '''
                    #?---------- 1 / 2 / 3 ---------- 
                    #costo_man = form.cleaned_data['costo_man']
                    fecha_entrega = datetime.now()
                    #?---------- 4 ---------- 
                    new_ficha = form.save(commit=False)
                    new_ficha.fecha_salida_man = fecha_entrega
                    #new_ficha.costo_man = costo_man
                    new_ficha.estado_man ='Entregado'
                    form.save()
                    #!---------- 5 ---------- falta desarollar

                    messages.success(request,"Se ha cambiado a - Entregado - el estado de la ficha.")
                    return HttpResponseRedirect(reverse_lazy('mantenimiento_detalle', kwargs=kwargs ))
                #---- Cuando el estado es Ingresado
                else:
                    messages.warning(request,"No se Puede poner en Ingresado a una ficha que ya esta Ingresada.")
                    return HttpResponseRedirect(reverse_lazy('mantenimiento_detalle', kwargs=kwargs ))
        else:
            #---- Cuando no es valido el formulario ----
            messages.error(request,"Existio un problema con tus campos revisalos antes de Guardarlos.")
            return self.render_to_response(self.get_context_data(form=form))


#todo====================================================================================================
#todo------------------------------ Mantenimientos para Tecnicos ----------------------------------------
#todo====================================================================================================
#todo--- Listado de los mantenimientos asignagos a cada teccnico ----------------------------------------
#todo----------------------------------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class Mantenimientos_Asignados(SuccessMessageMixin, TemplateView):
    template_name = 'dashboard/mantenimiento/tecnicos/mantenimiento_asignados.html'
    model = Mantenimiento
    
    def get_context_data(self, *args, **kwargs):
        #------------------------- Datos de Header ------------------------
        info_personal = self.request.user.first_name+' '+self.request.user.last_name
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #------------------------------------------------------------------
        pk_tecnico = self.request.user.id
        pk_perfil = Perfil.objects.get(usuario_id = pk_tecnico)
        #------------------------------------------------------------------
        fichas = Mantenimiento.objects.filter(usuario = pk_perfil.id, estado_man='Ingresado')
        return {
            'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido,
            'fichas':fichas,
            }


#todo====================================================================================================
#todo--- Listado del Historial de los mantenimientos asignagos a cada teccnico --------------------------
#todo----------------------------------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class Mantenimientos_Historial(SuccessMessageMixin, TemplateView):
    template_name = 'dashboard/mantenimiento/tecnicos/mantenimiento_historial.html'
    model = Mantenimiento
    
    def get_context_data(self, *args, **kwargs):
        #------------------------- Datos de Header ------------------------
        info_personal = self.request.user.first_name+' '+self.request.user.last_name
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #------------------------------------------------------------------
        pk_tecnico = self.request.user.id
        pk_perfil = Perfil.objects.get(usuario_id = pk_tecnico)
        #------------------------------------------------------------------
        #fichas = Mantenimiento.objects.filter(usuario = pk_perfil.id ,estado_man='Finalizado')
        fichas = Mantenimiento.objects.filter(Q(estado_man='Finalizado') | Q(estado_man='Entregado'))
        
        return {
            'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido,
            'fichas':fichas,
            }

#todo====================================================================================================
#todo------------------------ Listado de mantenimientos en taller o en Proceso --------------------------
#todo----------------------------------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class Mantenimientos_Proceso(SuccessMessageMixin, TemplateView):
    template_name = 'dashboard/mantenimiento/tecnicos/mantenimiento_proceso.html'
    model = Mantenimiento
    
    def get_context_data(self, *args, **kwargs):
        #------------------------- Datos de Header ------------------------
        info_personal = self.request.user.first_name+' '+self.request.user.last_name
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #------------------------------------------------------------------
        pk_tecnico = self.request.user.id
        pk_perfil = Perfil.objects.get(usuario_id = pk_tecnico)
        #------------------------------------------------------------------
        fichas = Mantenimiento.objects.filter(usuario = pk_perfil.id, estado_man='En Proceso')
        return {
            'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido,
            'fichas':fichas,
            }


#todo====================================================================================================
#todo----------------- Finalizar el mantenimiento cambiando el Estado de la Ficha -----------------------
#todo====================================================================================================
#todo----- Se cambia el estado del mantenimiento a Finalizado -------------------------------------------
#todo----- Se genera la fecha en la que se modifico y se la almacena en variable ------------------------
#todo----- Se obtiene y validad los datos del form (Procedimiento y observacione)------------------------
#todo----- Se almacenan los datos en la bbd y se notifica que se finalizo -------------------------------
#todo----------------------------------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class Ficha_Finalizar(SuccessMessageMixin, UpdateView):
    model = Mantenimiento
    template_name = 'dashboard/mantenimiento/gestion_fichas/tecnico/ficha_finalizar.html'
    form_class = Ficha_Finalizar_Form

    def get_context_data(self,**kwargs):
        context = super(Ficha_Finalizar, self).get_context_data(**kwargs)
        pk_ficha_editar = self.kwargs.get('pk', 0)
        ficha_editar = self.model.objects.get(id = pk_ficha_editar)
        if 'form' not in context:
            context['form'] = self.form_class(instance =ficha_editar)
        #------------------------- Datos de Header ------------------------
        info_personal = self.request.user.first_name+' '+self.request.user.last_name
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #------------------------------------------------------------------
        context['info_personal'] = info_personal
        context['avatar'] = avatar
        context['nombre_apellido'] = nombre_apellido
        context['ficha'] = ficha_editar
        context['id'] = pk_ficha_editar
        messages.warning(self.request,"Presta mucha Atención con los datos que se van a Ingresar.")
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_ficha = kwargs['pk']
        ficha_datos = self.model.objects.get(id = id_ficha)
        form = self.form_class(request.POST, instance = ficha_datos)
        
        if form.is_valid():
            
            #?---------- 1 / 2 / 3 ---------- 
            #estado_ficha = form.cleaned_data['procedimiento_man']
            costo_ficha = form.cleaned_data['costo_man']
            fecha_salida = datetime.now()
            #?---------- 4 ---------- 
            new_ficha = form.save(commit=False)
            new_ficha.fecha_salida_man = fecha_salida
            new_ficha.costo_man = costo_ficha
            new_ficha.estado_man ='Finalizado'
            form.save()

            messages.success(request,"Se Finalizo Correctamente el Mantenimiento.")
            return HttpResponseRedirect(reverse_lazy('mantenimiento_detalle', kwargs=kwargs ))
        
        else:
            #---- Cuando no es valido el formulario ----
            messages.error(request,"Existio un problema con tus campos revisalos antes de Guardarlos.")
            return self.render_to_response(self.get_context_data(form=form))


#todo====================================================================================================
#todo----------------- Entregar el mantenimiento cambiando el Estado de la Ficha -----------------------
#todo====================================================================================================
#todo----- Se cambia el estado del mantenimiento a Entregado --------------------------------------------
#todo----- Se genera la fecha en la que se entrega y se la almacena en variable -------------------------
#todo----- Se obtiene y valida los datos del form (Procedimiento y observacione) ------------------------
#todo----- Se almacenan los datos en la bbd y se notifica que se finalizo -------------------------------
#todo----------------------------------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class Ficha_Entregar(SuccessMessageMixin, UpdateView):
    model = Mantenimiento
    template_name = 'dashboard/mantenimiento/gestion_fichas/ventas/ficha_entregar.html'
    form_class = Ficha_Entrega_Form

    def get_context_data(self,**kwargs):
        context = super(Ficha_Entregar, self).get_context_data(**kwargs)
        pk_ficha_editar = self.kwargs.get('pk', 0)
        ficha_editar = self.model.objects.get(id = pk_ficha_editar)
        if 'form' not in context:
            context['form'] = self.form_class(instance =ficha_editar)
        #------------------------- Datos de Header ------------------------
        info_personal = self.request.user.first_name+' '+self.request.user.last_name
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]

        #------------------------------------------------------------------

        context['info_personal'] = info_personal
        context['avatar'] = avatar
        context['nombre_apellido'] = nombre_apellido
        context['ficha'] = ficha_editar
        context['id'] = pk_ficha_editar
        messages.warning(self.request,"Presta mucha Atención con los datos que se van a Ingresar.")
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_ficha = kwargs['pk']
        ficha_datos = self.model.objects.get(id = id_ficha)
        form = self.form_class(request.POST, instance = ficha_datos)

        if form.is_valid():
            #?---------- 1 / 2 / 3 ---------- 
            #costo_ficha = form.cleaned_data['costo_man']
            fecha_salida = datetime.now()
            #print(costo_ficha,'--------',fecha_salida,'--------',ficha_datos.cliente.email_cliente)
            #?---------- 4 ---------- 
            new_ficha = form.save(commit=False)
            new_ficha.fecha_salida_man = fecha_salida
            #new_ficha.costo_man = costo_ficha
            new_ficha.estado_man ='Entregado'
            #form.save()
            #?--------- notificacion al correo del cliente ----------
            Send_Email_Entrega(ficha_datos)
            #?-------------------------------------------------------
            messages.success(request,"Se Entrego Correctamente el Equipo y la ficha digital de mantenimiento al Cliente.")
            return HttpResponseRedirect(reverse_lazy('mantenimiento_detalle', kwargs=kwargs ))
        
        else:
            #---- Cuando no es valido el formulario ----
            messages.error(request,"Existio un problema con tus campos revisalos antes de Guardarlos.")
            return self.render_to_response(self.get_context_data(form=form))

#todo ---------------- Envio de Ficcha al correo CLiente ------------------
def Send_Email_Entrega(ficha_datos ):
    #? Guardar datos en context para pasar la informacion
    context = {'ficha_datos':ficha_datos}
    #? Obtencion del template y envio del contexto con la informacion
    template = get_template('dashboard/correos/correo_notificacion.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Notificación de Informacion de CPS.', #titulo de correo
        'Notificación de Entrega del Equipo de Mantenimiento. ', #descripcion del correo
        settings.EMAIL_HOST_USER, #cuenta desde donde se envia
        [ficha_datos.cliente.email_cliente],#destinatario
        #cc=[settings.EMAIL_HOST_USER],#cc=copia a
    )
    email.attach_alternative(content, "text/html")
    email.send()
    #? Adjuntar el pdf de la ficha
    #msg.attach_file(file_path)
    #msg.attach_file('files/media/myexcel.xlsx')
    '''
    now = datetime.now() 
    admin = User.objects.get(is_superuser = True)
    ficha = ficha_datos
    user = User.objects.get(is_superuser = True)
    data = {
            'fecha':now,
            'admin':admin,
            'ficha':ficha,
            'user':user,
            }

    pdf = render_to_pdf('dashboard/pdf/pdf_ficha.html', data)
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "Reporte_Prestamos.pdf"
    content = "attachment; filename=%s" %(filename)
    response['Content-Disposition'] = content
    #return HttpResponse(pdf, content_type='application/pdf')
    #email.attach('IMran_1066.pdf',response.read(),mimetype="application/pdf")
    email.attach(filename, content,mimetype="application/pdf")
    
    

    email.attach("document.pdf", res.rendered_content)
    '''
    '''
    now = datetime.now() 
    admin = User.objects.get(is_superuser = True)
    ficha = ficha_datos
    user = User.objects.get(is_superuser = True)
    data = {
            'fecha':now,
            'admin':admin,
            'ficha':ficha,
            'user':user,
            }

    pdf = render_to_pdf('dashboard/pdf/pdf_ficha.html',data)
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "Reporte_Prestamos.pdf"
    content = "attachment; filename=%s" %(filename)
    response['Content-Disposition'] = content
    email.attach(filename,response,'application/pdf')
    email.send()
    '''
@login_required
def correo_prueba(request):
    ficha_datos = Mantenimiento.objects.get(id=9)
    return render(request, 'dashboard/correos/correo_notificacion.html', {'ficha_datos':ficha_datos})



#todo====================================================================================================
#todo----------------- Generar PDF con los detalles de la Ficha de Mantenimiento -----------------------
#todo====================================================================================================

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

class ViewPDF_Ficha(View):

    def get(self, request, *args, **kwargs):
        pk_ficha = kwargs.get('pk', 0)
        user = self.request.user
        ficha = Mantenimiento.objects.get(id=pk_ficha)
        
        #prestamo = Prestamo.objects.get(id = pk_prestamo)
        #datos_usuario = User.objects.get(id = prestamo.usuario_id)
        #documentos = Documento.objects.get(id = prestamo.documento_id)
        #proyectos = Proyecto.objects.get(id = documentos.proyecto_id)
        admin = User.objects.get(is_superuser = True)
        now = datetime.now() 

        data = {
            'fecha':now,
            'admin':admin,
            'ficha':ficha,
            'user':user,
            }

        pdf = render_to_pdf('dashboard/pdf/pdf_ficha.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

@login_required
def ficha_pdf_prueba(request):
    ficha = Mantenimiento.objects.get(id=9)
    admin = User.objects.get(is_superuser = True)
    now = datetime.now() 
    return render(request, 'dashboard/pdf/pdf_ficha.html', {'fecha':now,'admin':admin,'ficha':ficha})