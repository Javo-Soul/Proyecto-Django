from django.http import JsonResponse, HttpResponseRedirect
from multiprocessing import context
from django.shortcuts import render, redirect
from core.erpbd.models import asignaciones, auditorias_diarias
from django.views.generic import CreateView, ListView, UpdateView
from core.erpbd.forms import AuditoriasDiariasForm, UpdateAsignacionesForm
from django.urls import reverse_lazy
import csv
from django.http import HttpResponse
import datetime
from datetime import datetime
# Create your views here.

####################### Formulario de Asignacion ##############
class Auditoriasdiariaslistview(ListView):
    model = auditorias_diarias
    template_name = 'auditoria/list.html'
    # aca podria editar la query !
    def get_queryset(self):
        return auditorias_diarias.objects.all().order_by('create_ts')[:100]
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
        context['action'] = 'add'
        return context

class AsignacionesUpdateView(UpdateView):
    model = asignaciones
    form_class = AuditoriasDiariasForm
    template_name = 'auditoria/create.html'
    success_url = reverse_lazy('auditorias')

##    def post(self,request, *args,**kwargs):
##        form = AuditoriasDiariasForm(request.POST)
##        if form.is_valid():
##            form.save()
##            return HttpResponseRedirect(self.success_url)
##        self.object = None
##        context = self.get_context_data(**kwargs)
##        context['form'] = form
##        return  render(request,self.template_name,context)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Auditorias'
        context['entity'] = 'auditorias'
        context['list_url'] = reverse_lazy('auditorias')
        context['action'] = 'edit'
        return context
####################### Formulario de Asignacion ##############


def buscaritem(request):
    #get trae respuesta de formulario
    #item = al "name" del formulario
    if request.GET["item"]:
            item = request.GET["item"]
            if len(item) > 6:
                print("No Aplica,if")
                return render(request, 'auditoria/list.html')
            if len(item) == 0:
                print("No Aplica,if 2")
                return render(request, 'auditoria/list.html')
            else:
                item_for = request.GET["item"]
                item_bd = auditorias_diarias.objects.filter(item_nbr=item_for)
                return render(request, 'auditoria/list.html', {"item_bd": item_bd, "query": item_for})
    else:
        return render(request, 'auditoria/list.html')


# export a excel
def export_csv_audit(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = auditorias' + \
                                      str(datetime.now().strftime('%Y-%m-%d %H:%M')) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['user', 'container_tag_id', 'container_stat_dsc', 'trip_create_date', 'location_id',
                     'item_nbr', 'create_ts'])

    auditorias = auditorias_diarias.objects.all()

    for audit in auditorias:
        writer.writerow([audit.user, audit.container_tag_id + '_', audit.container_stat_dsc
                        , audit.trip_create_date.strftime('%Y-%m-%d %H:%M'),audit.location_id
                        , audit.item_nbr, audit.create_ts.strftime('%Y-%m-%d %H:%M')])

    return response