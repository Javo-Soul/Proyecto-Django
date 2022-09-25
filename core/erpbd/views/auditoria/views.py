from django.http import JsonResponse
from multiprocessing import context
from django.shortcuts import render
from core.erpbd.models import asignaciones, auditorias_diarias
from django.views.generic import CreateView,ListView,UpdateView
from core.erpbd.forms import AuditoriasDiariasForm,AsignacionesForm
from django.urls import reverse_lazy
# Create your views here.

class Auditoriasdiariaslistview(ListView):
    model = auditorias_diarias
    template_name = 'auditoria/list.html'
    # aca podria editar la query !
    def get_queryset(self):
        return auditorias_diarias.objects.all().order_by('create_ts')[:10]


    def get_context_data(self, **kwargs): # -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Auditorias'
        success_url = reverse_lazy('erpbd:auditorias')
        return context


class AuditoriasdiariasCreateView(CreateView):
    model = auditorias_diarias
    form_class = AuditoriasDiariasForm
    template_name = 'auditoria/create.html'
    success_url = reverse_lazy('auditorias')
    #permission_required = 'erp.change_category'
    #url_redirect = success_url


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creacion de Auditorias'
        context['entity'] = 'Categorias'
        #context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class AsignacionesUpdateView(UpdateView):
    model = asignaciones
    form_class = AsignacionesForm
    template_name = 'auditoria/create.html'
    success_url = reverse_lazy('erpbd:auditorias')
    #permission_required = 'erp.change_category'
    #url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Auditorias'
        context['entity'] = 'Categorias'
        #context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


def AsignacionAudi(request):
    return render(request,'ProyectoWebApp/base.html')


def buscaritem(request):
    #get trae respuesta de formulario
    #item = al "name" del formulario
    if request.GET["item"]:
            item = request.GET["item"]
            if len(item) > 6:
                print("No Aplica,if")
                return render(request,'auditoria/list.html')
            if len(item) == 0:
                print("No Aplica,if 2")
                return render(request,'auditoria/list.html')
            else:
                item_for = request.GET["item"]
                item_bd = auditorias_diarias.objects.filter(item_nbr = item_for)
                return render(request,'auditoria/list.html',{"item_bd":item_bd,"query":item_for})
    else:
        return render(request,'auditoria/list.html')