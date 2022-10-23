from django.http import JsonResponse,HttpResponseRedirect
from multiprocessing import context
from django.shortcuts import render, redirect
from core.erpbd.models import asignaciones, auditorias_diarias
from django.views.generic import CreateView,ListView,UpdateView
from core.erpbd.forms import AuditoriasDiariasForm,AsignacionesForm
from django.urls import reverse_lazy
# Create your views here.

####################### Formulario de Asignacion ##############
class Auditoriasdiariaslistview(ListView):
    model = auditorias_diarias
    template_name = 'auditoria/list.html'
    # aca podria editar la query !
    def get_queryset(self):
        return auditorias_diarias.objects.all().order_by('create_ts')[:50]

    def get_context_data(self, **kwargs): # -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Auditorias'
        context['list_url'] = reverse_lazy('auditorias')
        context['entity'] = reverse_lazy('auditorias')
        success_url = reverse_lazy('auditorias')
        return context

class AuditoriasdiariasCreateView(CreateView):
    model = auditorias_diarias
    form_class = AuditoriasDiariasForm
    template_name = 'auditoria/create.html'
    success_url = reverse_lazy('auditorias')
    #permission_required = 'erp.change_category'
    #url_redirect = success_url
    def post(self,request, *args,**kwargs):
        form = AuditoriasDiariasForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return  render(request,self.template_name,context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Asignación de Auditorias'
        context['entity'] = reverse_lazy('auditorias_create')
        return context

class AsignacionesUpdateView(UpdateView):
    model = asignaciones
    form_class = AsignacionesForm
    template_name = 'auditoria/create.html'
    success_url = reverse_lazy('erpbd:auditorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Auditorias'
        context['entity'] = 'Categorias'
        #context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
####################### Formulario de Asignacion ##############

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