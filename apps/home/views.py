from cProfile import label
import email
from importlib.resources import contents
from multiprocessing import context
from re import template
from django.shortcuts import render
#todo------------------ Para Busquedas --------------------------
from django.db.models import Q
from django.core.paginator import Paginator
#todo ----------------- Para seguridad URLS ----------------------
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
#todo ----------------- Para Vistas basadas en Clases ----------------
from django.views.generic import CreateView, ListView, DetailView, UpdateView, TemplateView, DeleteView, View
#todo ----------------- Para Mesnsajes en pantalla -------------
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
#todo ----------------- Llamada Formularios -------------------
from apps.home.forms import Contacto_form, Reporte_form, Reporte_form_ficha, Reporte_form_tecnico, form_consulta_ficha
#todo ----------------- Para Generar y Enviar Correo ---------------------------
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
#todo ----------------- Importar los modelos para querys -------------------------
from django.contrib.auth.models import User
from apps.usuario.models import Perfil
from apps.cliente.models import Cliente
from apps.mantenimiento.models import Mantenimiento
from apps.bodega.models import Bodega
from apps.recordatorios.models import Recordatorios
#todo------------------ Para reportes ----------------------------------
from datetime import tzinfo, timedelta, datetime, date
from django.db.models import Sum
#todo---------------- Para renderizar a pdf ------------------
from io import BytesIO
from django.views import View
from xhtml2pdf import pisa
from django.http import HttpResponse
#todo ---------------- Para JSON -----------------------------
import json
from django.db.models import Sum, Count
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

# Create your views here.
#todo----------------------------- PWA CPS -------------------------------------------------
def Buscador_offline(request):
    return render(request, 'home/offline/Buscador_offline.html')  

def getdata(request):
    result = Mantenimiento.objects.all()
    #jsondata = serializers.serialize('json',result, fields = ("username", "first_name", "last_name"))
    jsondata = serializers.serialize('json',result, fields = ("codigo_man", "estado_man", "fecha_ingreso_man", "tipo_man", "tipo_equipo_man", "costo_man", "cliente.nombre1_cliente",'usuario' ))
    #print(jsondata)
    return HttpResponse(jsondata)

#? -- Pagina de Catalogos --
def catalogos(request):
    return render(request, 'home/catalogos/catalogos.html')

#todo--------------------------- Funciones para paginas principales -------------------------
def index(request):
    return render(request, 'index.html')

#? -- Pagina de inicio principal --
def index_home(request):
    return render(request, 'home/index_home.html')

#? -- Pagina de inicio dashboard --
def index_dashboard(request):
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    recordatorios = Recordatorios.objects.all()

    mantenimientos = Mantenimiento.objects.all().count()
    man_entregar = Mantenimiento.objects.filter(estado_man = 'Finalizado').count()
    man_taller = Mantenimiento.objects.filter(estado_man = 'En Proceso').count()
    
    year = year = datetime.now().year

    labels = []
    data = []

    #ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year).order_by('fecha_ingreso_man')

    months = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
        
    n_mes = {}

    cantidad = 0
    m = 0
        
    labels = []
    data = []

        
    fichas = Mantenimiento.objects.filter(fecha_ingreso_man__year = year).order_by('fecha_ingreso_man')
    for i in months:
        m=m+1
        labels.append(i)
        for y in fichas:
            if m == y.fecha_ingreso_man.month:
                cantidad=cantidad+1
        #n_mes.setdefault(i,cantidad)
        data.append(cantidad)
        cantidad = 0
    



    data_info = {
        'recordatorios':recordatorios,
        'avatar': avatar,
        'info_personal': info_personal,
        'nombre_apellido': nombre_apellido,
        'mantenimientos' : mantenimientos,
        'man_entregar' : man_entregar,
        'man_taller' : man_taller,
        'year':year,
        'labels': labels,
        'data': data,
    }

    return render(request, 'dashboard/index_dashboard.html', data_info)

#todo---------------------------- Pagina para consulta de fichas Clientes -------------------

#? -- Pagina de inicio principal --
def Consulta_Cliente(request):
    if request.method == 'POST':
        form = form_consulta_ficha(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo_ficha']
            
            ficha = Mantenimiento.objects.all()
            codigo_ficha1 = 0
            flag = 2
            for i in ficha:
                if i.codigo_man == codigo:
                    flag = 1
                    codigo_ficha1 = i
                    

            return render(request, 'home/cliente/consulta_cliente.html',{ 'form': form, 'flag':flag, 'codigo_ficha':codigo_ficha1, 'codigo':codigo })
        else:
            messages.error(request,"Ha existido un problema con los datos ingresados favor revise los campos.")
            return render(request, 'home/cliente/consulta_cliente.html',{ 'form': form })
    else:
        form = form_consulta_ficha()
        #messages.info(request, "Verifique y confirme los datos ingresados antes de enviarlos. GRACIAS.")
        return render(request, 'home/cliente/consulta_cliente.html',{ 'form': form })


#todo --------------------------- funcion envio de correo contactenos ------------------------
def contactenos(request):
    if request.method == 'POST':
        form = Contacto_form(request.POST)
        if form.is_valid():
            #?---------- Obtener datos del formulario ------------------
            # nombre = request.POST.get('nombre_completo')
            nombre = form.cleaned_data['nombre_completo']
            correo = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']
            telefono = form.cleaned_data['telefono']
            #?--------- Proceso de envio al administrador ---------------
            Send_Email_Contactenos(nombre, correo, telefono, mensaje)
            #?--------- Fin proceso enviar al administrador -------------
            messages.success(request,"Se ha enviado tu consulta al administrador correctamente, Se te respondera a tu correo lo más pronto posible Gracias.")
            form = Contacto_form()
            return render(request, 'home/contactenos/contactenos.html',{ 'form': form })
        else:
            messages.error(request,"Ha existido un problema con los datos ingresados favor revise los campos.")
            return render(request, 'home/contactenos/contactenos.html',{ 'form': form })
    else:
        form = Contacto_form()
        messages.info(request, "Verifique y confirme los datos ingresados antes de enviarlos. GRACIAS.")
        return render(request, 'home/contactenos/contactenos.html',{ 'form': form })

#todo ---------------- Envio de Correo de contactenos al administrador ------------------
def Send_Email_Contactenos(nombre, correo, telefono, mensaje ):
    
    #? Guardar datos en context para pasar la informacion
    context = {'nombre':nombre , 'correo':correo, 'telefono':telefono, 'mensaje':mensaje}
    #? Obtencion del template y envio del contexto con la informacion
    template = get_template('home/formatos_correos/correo_contactos.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Notificación del Sistema CPS.', #titulo de correo
        'Notificación de Requerimiento de Soporte o Consulta. ', #descripcion del correo
        settings.EMAIL_HOST_USER, #cuenta desde donde se envia
        [settings.EMAIL_HOST_USER],#destinatario
        #cc=[settings.EMAIL_HOST_USER],#cc=copia a
    )
    email.attach_alternative(content, "text/html")
    email.send()


#todo--------------------------------------------------------------------------
#todo ---------------- Funciones de Busqueda en el dashboard ------------------
#todo--------------------------------------------------------------------------

#todo -- Pagina de inicio para las busquedas --
@login_required
def Busquedas_index(request):
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    
    return render(request, 'dashboard/busquedas/busqueda_index.html', {'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})

#todo -- Pagina para la Busqueda de Personal --
@login_required
def Busqueda_Usuario(request):
    #print(request.GET)
    #-------------- Datos para el Header del Usuario --------
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    #---------------------------- FIN -----------------------
    querySet = request.GET.get("buscar_usuario")
    if querySet:
        usuario = User.objects.all().filter(
            #Q(username__icontains = querySet) | 
            Q(first_name__icontains = querySet) |
            Q(last_name__icontains = querySet) |
            #Q(email__icontains = querySet) |
            Q(perfil__cedula_perfil__icontains = querySet)
        )
        return render(request, 'dashboard/busquedas/busqueda_usuario.html', {'usuario': usuario, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})
    else:
        return render(request, 'dashboard/busquedas/busqueda_usuario.html', {'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})


#todo -- Pagina para la Busqueda de Clientes --
@login_required
def Busqueda_Cliente(request):
    #print(request.GET)
    #-------------- Datos para el Header del Usuario --------
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    #---------------------------- FIN -----------------------
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
        return render(request, 'dashboard/busquedas/busqueda_cliente.html', {'cliente': cliente, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})
    else:
        return render(request, 'dashboard/busquedas/busqueda_cliente.html', {'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})


#todo -- Pagina para la Busqueda de Fichas de Mantenimiento --
@login_required
def Busqueda_Fichas(request):
    #print(request.GET)
    #-------------- Datos para el Header del Usuario --------
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    #---------------------------- FIN -----------------------
    querySet = request.GET.get("buscar_ficha")
    if querySet:
        ficha = Mantenimiento.objects.all().filter(
            Q(cliente__cedula_cliente__icontains = querySet) |
            Q(codigo_man__icontains = querySet) |
            Q(fecha_ingreso_man__icontains = querySet) |
            #Q(tipo_man__icontains = querySet) |
            Q(estado_man__icontains = querySet)
        )

        paginator = Paginator(ficha, 5) # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'dashboard/busquedas/busqueda_mantenimiento.html', {'page_obj': page_obj, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})
    else:
        return render(request, 'dashboard/busquedas/busqueda_mantenimiento.html', {'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})


#todo=======================================================================================================
#todo------------------------------------ Servicio de Reportes ---------------------------------------------
#todo=======================================================================================================

#todo -- Pagina de inicio para los Reportes --
@login_required
def Reporte_index(request):
    #-------------------- Datos de Header --------------------------------------
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    #----- color de avatar (circulo) --------------------------------------------
    import random
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    
    return render(request, 'dashboard/reportes/reportes_index.html', {'color':color,'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})

#todo -- Genera reporte de Clientes mensuales o anuales que han realizado mantenimiento
@login_required
def Reporte_Cliente(request):
    #----------------------------- Datos de Header --------------------------------------
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    #-------------------------------------------------------------------------------------

    #?---------- Presentacion del formulario --------------
    if request.method == 'POST':
        form = Reporte_form(request.POST)
        if form.is_valid():
            #? Obtencion de los datos del formulario
            mes = form.cleaned_data['meses']
            year = form.cleaned_data['year'] 
            

            if mes == '0' :
                ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year).order_by('fecha_ingreso_man')
                cantidad = Mantenimiento.objects.filter(fecha_ingreso_man__year = year).count
            else:
                ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes).order_by('fecha_ingreso_man')
                cantidad = Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes).count()

            year=int(year)

            if ficha:
                messages.success(request, "Se han encontrado los datos correctamente")
            else:
                messages.info(request, "No se encoontraron datos con las fechas ingresadas")

            return render(request, 'dashboard/reportes/reporte_cliente.html', {'form': form, 'ficha':ficha,'year':year,'mes':mes, 'cantidad':cantidad, 'avatar': avatar,'info_personal': info_personal, 'nombre_apellido':nombre_apellido})  
        else:
            messages.error(request, "Existio un problema con los datos, vuelva a intentarlo")
            cliente={}
            return render(request, 'dashboard/reportes/reporte_cliente.html', {'form': form, 'ficha':ficha, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})  
    else:
        cliente = {}
        form = Reporte_form()
        return render(request, 'dashboard/reportes/reporte_cliente.html',{'form': form, 'cliente':cliente, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})  


#todo -- Genera reporte de los tecnicos con mantenimientos 
@login_required
def Reporte_Tecnico(request):
    #----------------------------- Datos de Header --------------------------------------
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    #-------------------------------------------------------------------------------------
    #?---------- Presentacion del formulario --------------
    if request.method == 'POST':
        form = Reporte_form_tecnico(request.POST)
        if form.is_valid():
            #? Obtencion de los datos del formulario
            year = form.cleaned_data['year']
            mes = form.cleaned_data['meses']
            tecnico = form.cleaned_data['tecnico'] 

            if tecnico == None:
                id_tecnico = 0
            else:
                id_tecnico = tecnico.id
            #? Consulta de los datos

            if mes == '0' and tecnico == None :
                #print('se imprimen todos los tecnicos con mantenimientos de todos los meses')
                tecnico1 = Perfil.objects.filter(cargo_perfil__icontains = 'Técnico' )
                ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year).order_by('fecha_ingreso_man')
            elif mes != '0' and tecnico == None :
                #print('impime los todos los tecnicos del mes selecionado')
                ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes).order_by('fecha_ingreso_man')
                tecnico1 = Perfil.objects.filter(cargo_perfil__icontains = 'Técnico' )
            elif mes == '0' and tecnico != None:
                #print('se imprime las fichas de todos los meses del tecnico elegido')
                ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year).order_by('fecha_ingreso_man')
                tecnico1 = Perfil.objects.filter(id = tecnico.id )
            elif mes != '0' and tecnico != None:
                #print('se imprime el tecnico seleccionado con las fichas del mes seleccionado')
                ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes).order_by('fecha_ingreso_man')
                tecnico1 = Perfil.objects.filter(id = tecnico.id )
            else:
                ficha = {}
                tecnico1 = {}
                #print('datos incorrectos')
            year=int(year)

            if ficha:
                messages.success(request, "Se han encontrado los datos correctamente")
            else:
                messages.info(request, "No se encoontraron datos con las fechas ingresadas")

            #? -- Envio de datos al Template y formulario --

            return render(request, 'dashboard/reportes/reporte_tecnico.html', {'ficha':ficha, 'id_tecnico':id_tecnico, 'tecnico':tecnico,'tecnico1':tecnico1, 'year':year, 'mes':mes, 'form': form, 'avatar': avatar,'info_personal': info_personal, 'nombre_apellido':nombre_apellido})  
        else:
            messages.error(request, "Existio un problema con los datos, vuelva a intentarlo")
            return render(request, 'dashboard/reportes/reporte_tecnico.html', {'form': form, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})  
    else:
        form = Reporte_form_tecnico()
        return render(request, 'dashboard/reportes/reporte_tecnico.html',{'form': form, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})  




#todo -- Genera reporte de los fichas de mantenimientos 
@login_required
def Reporte_Fichas(request):
    #----------------------------- Datos de Header --------------------------------------
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    #-------------------------------------------------------------------------------------
    #?---------- Presentacion del formulario --------------
    if request.method == 'POST':
        form = Reporte_form_ficha(request.POST)
        if form.is_valid():
            #? Obtencion de los datos del formulario
            year = form.cleaned_data['year']
            mes = form.cleaned_data['meses']
            #estado = form.cleaned_data['estados']  
            
            #? Consulta de los datos

            if mes == '0':
                #print('fichas de todos los meses')
                ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year).order_by('fecha_ingreso_man')
            elif mes != '0' :
                #print('todas las fichas del mes selecionado')
                ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes).order_by('fecha_ingreso_man')
            else:
                ficha={}
                print('datos incorrectos')

            if ficha:
                messages.success(request, "Se han encontrado los datos correctamente")
            else:
                messages.info(request, "No se encoontraron datos con las fechas ingresadas")

            #? -- Envio de datos al Template y formulario --
            year=int(year)
            return render(request, 'dashboard/reportes/reporte_ficha.html', {'year':year,'mes':mes,'ficha':ficha, 'form': form, 'avatar': avatar,'info_personal': info_personal, 'nombre_apellido':nombre_apellido})  
        else:
            messages.error(request, "Existio un problema con los datos, vuelva a intentarlo")
            return render(request, 'dashboard/reportes/reporte_ficha.html', {'form': form, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})  
    else:
        form = Reporte_form_ficha()
        return render(request, 'dashboard/reportes/reporte_ficha.html',{'form': form, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})  




#todo -- Genera reporte de los repuestos en bbodega
@login_required
def Reporte_Bodega(request):
    #----------------------------- Datos de Header --------------------------------------
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    #-------------------------------------------------------------------------------------
    #?---------- Presentacion del formulario --------------
    if request.method == 'POST':
        form = Reporte_form_ficha(request.POST)
        if form.is_valid():
            #? Obtencion de los datos del formulario
            year = form.cleaned_data['year']
            mes = form.cleaned_data['meses']
            #estado = form.cleaned_data['estados']  
            
            #? Consulta de los datos

            if mes == '0':
                #print('fichas de todos los meses')
                ficha = Bodega.objects.filter(fecha_pieza__year = year).order_by('fecha_pieza')
            elif mes != '0' :
                #print('todas las fichas del mes selecionado')
                ficha = Bodega.objects.filter(fecha_pieza__year = year, fecha_pieza__month = mes).order_by('fecha_pieza')
            else:
                ficha={}
                print('datos incorrectos')

            if ficha:
                messages.success(request, "Se han encontrado los datos correctamente")
            else:
                messages.info(request, "No se encoontraron datos con las fechas ingresadas")

            #? -- Envio de datos al Template y formulario --
            year=int(year)
            #? -- Envio de datos al Template y formulario --

            return render(request, 'dashboard/reportes/reporte_bodega.html', {'year':year,'mes':mes,'ficha':ficha, 'form': form, 'avatar': avatar,'info_personal': info_personal, 'nombre_apellido':nombre_apellido})  
        else:
            messages.error(request, "Existio un problema con los datos, vuelva a intentarlo")
            return render(request, 'dashboard/reportes/reporte_bodega.html', {'form': form, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})  
    else:
        form = Reporte_form_tecnico()
        return render(request, 'dashboard/reportes/reporte_bodega.html',{'form': form, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})  



#todo=================================================================================================================================
#todo------------------------------------------------- GENERAR PDF DE LOS REPORTES ---------------------------------------------------
#TODO=================================================================================================================================

#?---- Funcion para renderizar el PDF ----
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

#todo----------- Reporte Cliente PDF-----------------------------------

class pdf_reporte_cliente(View):

    def get(self, request, *args, **kwargs):
        
        mes = self.kwargs.get('mes', 0)
        year = self.kwargs.get('year', 0)
            
        months = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
        month = months[int(mes) - 1]
            
        if mes == 0 :
            ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year).order_by('fecha_ingreso_man')
            cantidad = Mantenimiento.objects.filter(fecha_ingreso_man__year = year).count
            
        else:
            ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes).order_by('fecha_ingreso_man')
            cantidad = Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes).count()
            
        year=int(year)
        
        data = {
            'ficha': ficha,
            'cantidad': cantidad,
            'month':month,
            'year':year,
            'mes':mes,
            }

        pdf = render_to_pdf('dashboard/reportes/pdf/pdf_reporte_cliente.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


#todo----------- Reporte Tecnico PDF-----------------------------------

class pdf_reporte_tecnico(View):

    def get(self, request, *args, **kwargs):
        
        mes = self.kwargs.get('mes', 0)
        year = self.kwargs.get('year', 0)
        tecnico = self.kwargs.get('id_tecnico', 0)
            
        months = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
        month = months[int(mes) - 1]

        fecha = datetime.now()

        #? Consulta de los datos
        caso = 0
        ganancia = 0

        if mes == 0 and tecnico == 0 :
            caso = 1
            print(caso,'------ caso')
            #print('se imprimen todos los tecnicos con mantenimientos de todos los meses')
            tecnico1 = Perfil.objects.filter(cargo_perfil__icontains = 'Técnico' )
            ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year).order_by('fecha_ingreso_man')
            ganancia =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year).aggregate(Sum('costo_man'))
            cantidad =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year).count()
            cantidad_entregado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, estado_man='Entregado' ).count()
            cantidad_finalizado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, estado_man='Finalizado' ).count()
            cantidad_taller =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, estado_man='En Proceso' ).count()
            cantidad_asignado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, estado_man='Ingresado' ).count()
        elif mes != 0 and tecnico == 0 :
            caso = 2
            print(caso,'------ caso')
            #print('impime los todos los tecnicos del mes selecionado')
            tecnico1 = Perfil.objects.filter(cargo_perfil__icontains = 'Técnico' )
            ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes).order_by('fecha_ingreso_man')
            ganancia =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes).aggregate(Sum('costo_man'))
            cantidad =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes).count()
            cantidad_entregado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes, estado_man='Entregado' ).count()
            cantidad_finalizado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes, estado_man='Finalizado' ).count()
            cantidad_taller =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes, estado_man='En Proceso' ).count()
            cantidad_asignado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes, estado_man='Ingresado' ).count()
        elif mes == 0 and tecnico != 0:
            caso = 3
            print(caso,'------ caso')
            #print('se imprime las fichas de todos los meses del tecnico elegido')
            tecnico1 = Perfil.objects.get(id = tecnico )
            ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year, usuario = tecnico1.id, estado_man = 'Entregado').order_by('fecha_ingreso_man')
            ganancia =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, usuario = tecnico1.id).aggregate(Sum('costo_man'))
            cantidad =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, usuario = tecnico1.id).count()
            cantidad_entregado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, usuario = tecnico1.id, estado_man='Entregado' ).count()
            cantidad_finalizado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, usuario = tecnico1.id, estado_man='Finalizado' ).count()
            cantidad_taller =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, usuario = tecnico1.id, estado_man='En Proceso' ).count()
            cantidad_asignado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, usuario = tecnico1.id, estado_man='Ingresado' ).count()
        elif mes != 0 and tecnico != 0:
            caso = 4
            print(caso,'------ caso')
            #print('se imprime el tecnico seleccionado con las fichas del mes seleccionado')
            tecnico1 = Perfil.objects.get(id = tecnico )
            ficha = Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes, usuario = tecnico1.id, estado_man = 'Entregado').order_by('fecha_ingreso_man')
            ganancia =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes, usuario = tecnico1.id ).aggregate(Sum('costo_man'))
            cantidad =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes, usuario = tecnico1.id ).count()
            cantidad_entregado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes, usuario = tecnico1.id, estado_man='Entregado' ).count()
            cantidad_finalizado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes, usuario = tecnico1.id, estado_man='Finalizado' ).count()
            cantidad_taller =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes, usuario = tecnico1.id, estado_man='En Proceso' ).count()
            cantidad_asignado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes, usuario = tecnico1.id, estado_man='Ingresado' ).count()
        else:
            ficha = {}
            tecnico1 = {}
            print('datos incorrectos')
            year=int(year)

        #?---------------- envio de datos ---------------------
        year=int(year)
        data = {
            'caso':caso,
            'fecha':fecha,
            'ganancia':ganancia['costo_man__sum'],
            'tecnico1':tecnico1,
            'ficha': ficha,
            'cantidad': cantidad,
            'cantidad_entregado':cantidad_entregado,
            'cantidad_asignado':cantidad_asignado,
            'cantidad_taller':cantidad_taller,
            'cantidad_finalizado':cantidad_finalizado,
            'month':month,
            'year':year,
            'mes':mes,
            }

        pdf = render_to_pdf('dashboard/reportes/pdf/pdf_reporte_tecnico.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

#todo----------- Reporte fichas PDF-----------------------------------

class pdf_reporte_fichas(View):

    def get(self, request, *args, **kwargs):
        
        mes = self.kwargs.get('mes', 0)
        year = self.kwargs.get('year', 0)
        #estado = self.kwargs.get('estado', 0)
            
        months = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
        month = months[int(mes) - 1]

        fecha = datetime.now()

        #? Consulta de los datos
        
        n_mes = {}
        ganancia_mes = {}
        '''
        for i in months:
            d_mes.setdefault(i)

        for i in d_mes:
            print (i, ":", d_mes[i])

        for i in n_mes:
                print (i, ":", n_mes[i])
        '''
        cantidad = 0
        total_mes = 0
        m = 0
        
        if mes == 0:
            caso = 1
            fichas = Mantenimiento.objects.filter(fecha_ingreso_man__year = year).order_by('fecha_ingreso_man')
            cantidad_total = Mantenimiento.objects.filter(fecha_ingreso_man__year = year).order_by('fecha_ingreso_man').count()
            for i in months:
                m=m+1
                for y in fichas:
                    if m == y.fecha_ingreso_man.month:
                        cantidad=cantidad+1
                        if y.costo_man != None:
                            total_mes=total_mes+y.costo_man
                n_mes.setdefault(i,cantidad)
                ganancia_mes.setdefault(i,total_mes)
                cantidad = 0
                total_mes = 0
            
            cantidad_entregado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year,estado_man='Entregado' ).count()
            cantidad_finalizado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year,estado_man='Finalizado' ).count()
            cantidad_taller =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year,estado_man='En Proceso' ).count()
            cantidad_asignado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year,estado_man='Ingresado' ).count()
            ganancia_entregado = Mantenimiento.objects.filter(fecha_ingreso_man__year = year,estado_man='Entregado' ).aggregate(Sum('costo_man'))
            ganancia_total = Mantenimiento.objects.filter(fecha_ingreso_man__year = year).aggregate(Sum('costo_man'))

        else:
            caso = 2
            fichas = Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes).order_by('fecha_ingreso_man')
            cantidad_total = Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes).order_by('fecha_ingreso_man').count()
            cantidad_entregado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes,estado_man='Entregado' ).count()
            cantidad_finalizado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes,estado_man='Finalizado' ).count()
            cantidad_taller =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes,estado_man='En Proceso' ).count()
            cantidad_asignado =  Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes,estado_man='Ingresado' ).count()
            ganancia_entregado = Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes,estado_man='Entregado' ).aggregate(Sum('costo_man'))
            ganancia_total = Mantenimiento.objects.filter(fecha_ingreso_man__year = year, fecha_ingreso_man__month = mes,).aggregate(Sum('costo_man'))

        
        
        
        #?---------------- envio de datos ---------------------
        year=int(year)
        data = {
            'caso':caso,
            'n_mes':n_mes,
            'cantidad_total':cantidad_total,
            'ganancia_mes':ganancia_mes,
            'ganancia_total':ganancia_total['costo_man__sum'],
            'ganancia_entregado':ganancia_entregado['costo_man__sum'],
            'cantidad_entregado':cantidad_entregado,
            'cantidad_asignado':cantidad_asignado,
            'cantidad_taller':cantidad_taller,
            'cantidad_finalizado':cantidad_finalizado,
            'fecha':fecha,
            'month':month,
            'year':year,
            'mes':mes,
            }

        pdf = render_to_pdf('dashboard/reportes/pdf/pdf_reporte_ficha.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

#todo=========================================================================
#todo-------------Página para la busqueda en Bodega------------------------
#todo=========================================================================

@login_required
def Busqueda_Bodega(request):
    info_personal = request.user.first_name+' '+request.user.last_name
    avatar = request.user.first_name[0:1]+request.user.last_name[0:1]
    lista_nombrecompleto= request.user.first_name.split()+request.user.last_name.split()
    nombre_apellido = lista_nombrecompleto[0]+' '+lista_nombrecompleto[2]
    querySet = request.GET.get("buscar_bodega")
    if querySet:
        bodega = Bodega.objects.all().filter(
            Q(nombre_pieza__icontains = querySet)|
            Q(serie_pieza__icontains = querySet)|
            Q(fecha_pieza__icontains = querySet)
        )
        return render(request, 'dashboard/busquedas/busqueda_bodega.html', {'bodega': bodega, 'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})
    else:
        return render(request,'dashboard/busquedas/busqueda_bodega.html', {'avatar': avatar, 'info_personal': info_personal, 'nombre_apellido':nombre_apellido})


#todo----------- Reporte bodega PDF-----------------------------------

class pdf_reporte_bodega(View):

    def get(self, request, *args, **kwargs):
        
        mes = self.kwargs.get('mes', 0)
        year = self.kwargs.get('year', 0)
        #estado = self.kwargs.get('estado', 0)
            
        months = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
        month = months[int(mes) - 1]

        fecha = datetime.now()

        #? Consulta de los datos
        
        if mes == 0:
            caso = 1
            ficha = Bodega.objects.filter(fecha_pieza__year = year).order_by('fecha_pieza')
            cantidad_total = Bodega.objects.filter(fecha_pieza__year = year).order_by('fecha_pieza').count()
        else:
            caso = 2
            ficha = Bodega.objects.filter(fecha_pieza__year = year, fecha_pieza__month = mes).order_by('fecha_pieza')
            cantidad_total = Bodega.objects.filter(fecha_pieza__year = year, fecha_pieza__month = mes).order_by('fecha_pieza').count()
        
        #?---------------- envio de datos ---------------------
        year=int(year)
        data = {
            'ficha':ficha,
            'caso':caso,
            'cantidad_total':cantidad_total,
            'fecha':fecha,
            'month':month,
            'year':year,
            'mes':mes,
            }

        pdf = render_to_pdf('dashboard/reportes/pdf/pdf_reporte_bodega.html', data)
        return HttpResponse(pdf, content_type='application/pdf')