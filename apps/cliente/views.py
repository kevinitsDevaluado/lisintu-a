from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponseRedirect
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
from apps import cliente
#todo ----------------- Llamada Formularios ----------------------
from apps.cliente.forms import ClienteForm
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

# Create your views here.

#todo--------------------------- Funciones para pagina principal ----------------------------
#todo------------------------------ Clientes de la Empresa ---------------------------------
@login_required
def cliente_index(request):
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    
    return render(request, 'dashboard/cliente/cliente_index.html', {'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})

#todo--------------------------- Funciones para listado de Clientes -------------------------
@login_required
def Cliente_Listado(request):
    #----- Informacion User Logeado ----
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    #----- Informacion User Logeado ----
    cliente = Cliente.objects.all().order_by("-id")
    return render(request, 'dashboard/cliente/cliente_listado.html',{
        'cliente':cliente,
        'avatar': avatar, 
        'nombre_apellido':nombre_apellido
        })

#todo-------------------------- Clase para Registrar un nuevo Cliente ------------------------

@method_decorator(login_required, name='dispatch')
class Cliente_Registrar(SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'dashboard/cliente/cliente_registrar.html'
    success_message = 'Se ha registrado correctamente al cliente'
    success_url = reverse_lazy('listado_clientes')

    def get_context_data(self, **kwargs):
        context = super(Cliente_Registrar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            usuario_ingresa=request.user.id
            new.usuario_id = usuario_ingresa
            form.save()
            nombre_cliente = new.nombre1_cliente+' '+new.apellido1_cliente
            messages.success(request,"Se ha registrado al cliente "+nombre_cliente)
            #print(new.nombre_proyecto, " - > Archivo ->", new.usuario_id)
            
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(request,"Existio un problema con tus campos revisalos")
            return self.render_to_response(self.get_context_data(form=form))


#todo-------------------------- Clase para ver detalle de Clientes ------------------------
# ---- Detalle de la informacion del cliente enviado como parametro el id del cliente ----
@method_decorator(login_required, name='dispatch')
class Cliente_Detail(SuccessMessageMixin, TemplateView):
    template_name = 'dashboard/cliente/cliente_detalle.html'
    def get_context_data(self, **kwargs):
        context = super(Cliente_Detail, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        cliente = Cliente.objects.get(id=pk)
        #----- Informacion User Logeado ----
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #----- Fin Informacion User Logeado ----
        return {'cliente': cliente, 'avatar': avatar, 'nombre_apellido':nombre_apellido}


#todo--------------------------- Funcion para eliminar al cliente -------------------------    
#---- Funcion para dar de baja al cliente solicitado enviando id como parametro por url ----
@method_decorator(login_required, name='dispatch')
class Cliente_Delete(SuccessMessageMixin, TemplateView):
    model = Cliente
    template_name = 'dashboard/usuario/usuario_eliminar.html'
    success_url = reverse_lazy('listado_usuarios')

    def get_context_data(self, **kwargs):
        context = super(Cliente_Delete, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        user1 = self.model.objects.get(id = pk)
        context['id'] = pk
        #----- Informacion User Logeado ----
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #----- Fin Informacion User Logeado ----
        messages.warning(self.request,"La acción que va a realizar es irreversible tome precausiones.")
        return {'personal': user1, 'avatar': avatar, 'nombre_apellido':nombre_apellido}

    def post(self, request, *args, **kwargs):
        id_cliente = kwargs['pk']
        estado = Cliente.objects.filter(id=id_cliente).update(estado_cliente=False)
        name_user = Cliente.objects.get(id = id_cliente)
        #print(estado)
        messages.success(self.request,"Se ha dado de baja al cliente "+ str(name_user.nombre1_cliente) + str(name_user.apellido1_cliente) +" "+" correctamente.")
        return HttpResponseRedirect(reverse_lazy('listado_clientes'))


#todo------------------------- Funcion para editar la infocion del personal ---------------------
# --- Clase para editar el usuario enviando 2 parametros el id_cliente y el id_admin ------------
@method_decorator(login_required, name='dispatch')
class Cliente_Update(SuccessMessageMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'dashboard/cliente/cliente_editar.html'
    
    def get_context_data(self,**kwargs):
        context = super(Cliente_Update, self).get_context_data(**kwargs)
        #------------------ obtengo id de la url -------------------
        pk_editar = self.kwargs.get('pk', 0)
        #----------------- consulta de datos del id a editar -------
        cliente_editar = self.model.objects.get(id = pk_editar)
        #-------- Instanciamos los datos en el form y los enviamos a pantalla ----
        if 'form' not in context:
            context['form'] = self.form_class(instance = cliente_editar)
        context['id'] = pk_editar
        #------------- informacion de header -----------------
        
        cliente = self.model.objects.get(id = pk_editar)
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        context['cliente'] = cliente
        context['avatar'] = avatar
        context['nombre_apellido'] = nombre_apellido
        messages.warning(self.request,"Presta mucha atención con los cambios que realices")
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_cliente = kwargs['pk']
        id_admin = kwargs['admin_pk']

        cliente2 = self.model.objects.get(id = id_cliente)
        form = self.form_class(request.POST, instance = cliente2)

        if form.is_valid():
            new = form.save(commit=False)
            a = new.id
            nombre = new.nombre1_cliente
            apellido = new.apellido1_cliente
            form.save()
            messages.success(request,"Se ha modificado los datos del usuario "+ str(nombre) + str(apellido) +" "+" correctamente.")
            #------- Consulta del usuario y logeo en la pagina ---------
            p_admin = User.objects.get(id=id_admin)
            usuario = authenticate(username=p_admin.username, password=p_admin.password)
            login(self.request, usuario)
            return HttpResponseRedirect(reverse_lazy('listado_clientes'))
        else:
            messages.error(request,"Existio un problema con tus campos revisalos")
            return self.render_to_response(self.get_context_data(form=form))