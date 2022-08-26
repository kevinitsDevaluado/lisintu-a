import email
from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponseRedirect, redirect
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
#from apps.home.forms import Contacto_form
from apps.usuario.forms import UpdatePerfilForm, UpdateUserForm, UserForm, PerfilForm
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


# Create your views here.

#todo--------------------------- Funciones para pagina principal ----------------------------
#todo------------------------------ Personal de la Empresa ---------------------------------
@login_required
def usuario_index(request):
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    
    return render(request, 'dashboard/usuario/usuario_index.html', {'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})


#todo--------------------------- Funciones para listado de Personal -------------------------
@method_decorator(login_required, name='dispatch')
class Usuario_Listado(SuccessMessageMixin, ListView):
    model = User
    template_name = 'dashboard/usuario/usuario_listado.html'
    def get_queryset(self):
            return User.objects.exclude(is_superuser=True, is_staff=True).order_by('id')

@login_required
def Usuario_Listado_funcion(request):
    #----- Informacion User Logeado ----
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    #----- Informacion User Logeado ----
    usuario = User.objects.exclude(is_superuser=True, is_staff=True).order_by('last_name')
    return render(request, 'dashboard/usuario/usuario_listado.html',{
        'usuario':usuario,
        'avatar': avatar, 
        'nombre_apellido':nombre_apellido
        })

#todo--------------------------- Funciones para detalle de Personal -------------------------    
# ---- Detalle de perfiles para que el administrador pueda ingresar ----
@method_decorator(login_required, name='dispatch')
class Usuario_Detail(SuccessMessageMixin, TemplateView):
    template_name = 'dashboard/usuario/usuario_detalle.html'
    def get_context_data(self, **kwargs):
        context = super(Usuario_Detail, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        personal = User.objects.get(id=pk)
        #----- Informacion User Logeado ----
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #----- Fin Informacion User Logeado ----
        return {'personal': personal, 'avatar': avatar, 'nombre_apellido':nombre_apellido}

#todo--------------------------- Funciones para eliminar al personal -------------------------    
#---- Funcion para dar de baja al personal solicitado enviando pk como parametro por url ----
@method_decorator(login_required, name='dispatch')
class Usuario_Delete(SuccessMessageMixin, TemplateView):
    model = User
    template_name = 'dashboard/usuario/usuario_eliminar.html'
    #success_message = 'Se ha dado de baja al usuario correctamente.'
    success_url = reverse_lazy('listado_usuarios')

    def get_context_data(self, **kwargs):
        context = super(Usuario_Delete, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        user1 = self.model.objects.get(id = pk)
        context['id'] = pk
        #print(user1.username)
        #----- Informacion User Logeado ----
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        #----- Fin Informacion User Logeado ----
        messages.warning(self.request,"La acción que va a realizar es irreversible tome precausiones.")
        return {'personal': user1, 'avatar': avatar, 'nombre_apellido':nombre_apellido}

    def post(self, request, *args, **kwargs):
        id_user = kwargs['pk']
        estado = User.objects.filter(id=id_user).update(is_active=False)
        name_user = User.objects.get(id = id_user)
        #print(estado)
        messages.success(self.request,"Se ha dado de baja al usuario "+ str(name_user.username) +" correctamente.")
        return HttpResponseRedirect(reverse_lazy('listado_usuarios'))

#todo------------------------- Funcion para editar la infocion del personal ---------------------
#---- Edita la informacion de un trabajador ingresando como administrador -----------------------
@login_required
def usuario_editar(request):
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    
    return render(request, 'dashboard/usuario/usuario_editar.html', {'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})

# --- Clase para editar el usuario enviando 2 parametros el personal y el admin -------------
# --- Usado actualmente ----
#@method_decorator(login_required, name='dispatch')
class Usuario_Update(SuccessMessageMixin, UpdateView):
    model = User
    second_model = Perfil
    template_name = 'dashboard/usuario/usuario_editar.html'
    form_class = UpdateUserForm
    second_form_class = UpdatePerfilForm

    def get_context_data(self,**kwargs):
        context = super(Usuario_Update, self).get_context_data(**kwargs)
        pk_editar = self.kwargs.get('pk', 0)
        #------------------ obtengo id url -------------------
        usuario_editar = self.model.objects.get(id = pk_editar)
        usuario_editar_perfil= self.second_model.objects.get(usuario_id = usuario_editar.id)
        #----------------- consulta de datos -----------------
        if 'form' not in context:
            context['form'] = self.form_class(instance = usuario_editar)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance = usuario_editar_perfil)
        context['id'] = pk_editar
        #------------- informacion de header -----------------
        pk_personal=self.request.user.id # esta el id del logeado
        personal= self.model.objects.get(id = pk_personal)
        info_personal = self.request.user.first_name+' '+self.request.user.last_name
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        context['personal'] = personal
        context['avatar'] = avatar
        context['nombre_apellido'] = nombre_apellido
        messages.warning(self.request,"Presta mucha atención con los cambios que realices")
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_user = kwargs['pk']
        id_admin = kwargs['admin_pk']
        user2 = self.model.objects.get(id = id_user)
        usuario2 = self.second_model.objects.get(usuario_id = user2.id)

        form = self.form_class(request.POST, instance = user2)
        form2 = self.second_form_class(request.POST, instance = usuario2)

        if form.is_valid() and form2.is_valid():
            new = form.save(commit=False)
            new2 = form2.save(commit=False)
            form.save()
            form2.save()
            messages.success(request,"Se ha modificado los datos del usuario  "+ str(new.username) +" correctamente")
            p_admin = User.objects.get(id=id_admin)
            usuario = authenticate(username=p_admin.username, password=p_admin.password)
            login(self.request, usuario)
            #return HttpResponseRedirect(reverse_lazy('listado_usuarios'))
            if p_admin.is_staff:
                return HttpResponseRedirect(reverse_lazy('listado_usuarios'))
            else:
                #return HttpResponseRedirect(reverse_lazy('perfil_usuarios', id_user))
                return redirect('perfil_usuarios', id_user)
        else:
            #return HttpResponseRedirect(self.get_success_url())
            form.errors
            form2.errors
            messages.error(request,"Existio un problema con el proceso")
            #return HttpResponseRedirect(reverse_lazy('listado_usuarios'))
            return self.render_to_response(self.get_context_data(form=form, form2=form2))


#todo------------------------- Funcion de registro de personal -------------------------
#-------------------------------Registrar Usuarios -------------------------------------
#---- clase para registrar un trabajador en el sistema ----

@method_decorator(login_required, name='dispatch')
class SignUpView(SuccessMessageMixin, generic.CreateView):

    def userlog(request):
        a=request.user.id
        id_usuario=User.objects.get(id=a)
        print(id_usuario.id)
        a=UserLogeado_u=id_usuario.username
        b=UserLogeado_p=id_usuario.password
        return a,b

    # modelos de datos
    model = User
    second_model = Perfil
    # Formularios de datos
    form_class = UserForm
    second_form_class = PerfilForm
    # success forms
    template_name = 'registration/sign_up.html'
    success_url = reverse_lazy('listado_usuarios')

    def get_context_data(self, **kwargs): #pinto el formulario en el html
        context = super(SignUpView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        #------------- informacion de header -----------------
        pk_personal=self.request.user.id # esta el id del logeado
        personal= self.model.objects.get(id = pk_personal)
        info_personal = self.request.user.first_name+' '+self.request.user.last_name
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        context['personal'] = personal
        context['avatar'] = avatar
        context['nombre_apellido'] = nombre_apellido
        #-------------- Termina informacion header ------------
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            new = form.save()
            a = new.id
            id_detalle = new.id
            new2 = form2.save(commit=False)
            new2.usuario_id = a
            b = new2.usuario_id
            form2.save()
            messages.success(request,"Se ha registrado el usuario")
            print(a, " - > Usuario")
            print(b, " - > Datos Personales")

            usuario = authenticate(username=a, password=b)
            login(self.request, usuario)
            
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))
