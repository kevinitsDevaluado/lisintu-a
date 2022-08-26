from audioop import reverse
from multiprocessing import context
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import (CreateView, 
ListView, DetailView, 
UpdateView, TemplateView, 
DeleteView, View)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect,redirect,get_object_or_404
from apps.recordatorios.forms import Recordatorios_form
from apps.recordatorios.models import Recordatorios
# Create your views here.
def recordatorios_index(request):
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    
    return render(request, 'dashboard/recordatorios/recordatorios_index.html', {'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})

@method_decorator(login_required, name='dispatch')
class recordatorios_ingreso(CreateView):
    model = Recordatorios
    form_class = Recordatorios_form
    template_name = 'dashboard/recordatorios/recordatorios_ingreso.html'
    success_url = reverse_lazy('recordatorios_index')
    
    def get_context_data(self, **kwargs):
        context = super(recordatorios_ingreso,self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form']=self.form_class(self.request.GET)
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
            messages.success(request,"Se ha registrado el recordatorio ")
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(request,"Existio un problema con tus campos revisalos")
            return self.render_to_response(self.get_context_data(form=form))
@login_required
def Recordatorios_Listado(request):
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    recordatorios = Recordatorios.objects.all()
    return render(request,'dashboard/recordatorios/recordatorios_consulta.html',{'recordatorios':recordatorios,'avatar': avatar,'nombre_apellido':nombre_apellido})


class Recordatorio_Delete(SuccessMessageMixin, TemplateView):
    model = Recordatorios
    form_class = Recordatorios_form
    template_name = 'dashboard/recordatorios/recordatorios_eliminar.html'
    success_url = reverse_lazy('listado_usuarios')

    def get_context_data(self, **kwargs):
        context = super(Recordatorio_Delete, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        rec1 = self.model.objects.get(id = pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=rec1)
        context['id'] = pk

        cliente = self.model.objects.get(id = pk)
        avatar = self.request.user.first_name[0:1]+self.request.user.last_name[0:1]
        lista_nombrecompleto= self.request.user.first_name.split()+self.request.user.last_name.split()
        nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
        context['cliente'] = cliente
        context['avatar'] = avatar
        context['nombre_apellido'] = nombre_apellido
        context['recordatorio'] = rec1
        print(context)
        messages.warning(self.request,"La acción que va a realizar es irreversible tome precausiones.")
        return context

    def post(self, request, *args, **kwargs):
        id_rec = kwargs['pk']
        rec = Recordatorios.objects.get(id = id_rec).delete()
        #print(estado)
        messages.success(self.request,"Se ha dado eliminado el recordatorio ")
        return HttpResponseRedirect(reverse_lazy('recordatorios_consulta'))