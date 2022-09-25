from django.shortcuts import render,HttpResponse
from django.http import HttpResponse


# Create your views here.
################# Paginas de Inicio ######################################
def admin(request):
    return render(request,'/admin')

def asignacion_auditorias(request):
    return render(request,'admin/ProyectoWebApp/asignacione/')

def configuracion(request):
    return render(request,'admin/auth/user/1/change/#general-tab')