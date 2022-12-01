from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from multiprocessing import context
from django.shortcuts import render, redirect
from core.erpbd.models import asignaciones, auditorias_diarias
from django.views.generic import CreateView, ListView, UpdateView
from core.erpbd.forms import AuditoriasDiariasForm, UpdateResolucionForm
from django.urls import reverse_lazy

from core.erpbd.mixins import IsSuperuserMixin
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.http import HttpResponse

import datetime
from datetime import datetime
import csv
# Create your views here.

####################### Formulario de Asignacion ##############
class Auditoriasdiariaslistview(PermissionRequiredMixin,ListView):
    permission_required = 'erpbd.view_auditorias_diarias'
    model = auditorias_diarias
    template_name = 'auditoria/list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # aca podria editar la query !
    def get_queryset(self):
        lista_auditoria = auditorias_diarias.objects.filter(container_stat_dsc='Closed'
                                                            ).order_by('-last_change_ts')[:1000]
        return lista_auditoria
    def get_context_data(self, **kwargs): # -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Auditorias'
        context['list_url'] = reverse_lazy('auditorias')
        context['entity'] = reverse_lazy('auditorias')
        success_url = reverse_lazy('auditorias')
        return context

class AuditoriasdiariasCreateView(LoginRequiredMixin,IsSuperuserMixin,PermissionRequiredMixin,CreateView):
    permission_required = ('erpbd.view_auditorias_diarias', 'erpbd.change_auditorias_diarias','erpbd.create_auditorias_diarias')
    model = auditorias_diarias
    form_class = AuditoriasDiariasForm
    template_name = 'auditoria/create.html'
    success_url = reverse_lazy('auditorias')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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

class AsignacionesUpdateView(PermissionRequiredMixin,IsSuperuserMixin,UpdateView):
    permission_required = ('erpbd.view_auditorias_diarias','erpbd.change_auditorias_diarias')
    model = auditorias_diarias
    form_class = AuditoriasDiariasForm
    template_name = 'auditoria/create.html'
    success_url = reverse_lazy('auditorias')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Asignación de Auditorias'
        context['entity'] = 'auditorias'
        context['list_url'] = reverse_lazy('auditorias')
        context['action'] = 'edit'
        return context
####################### Formulario de Asignacion ##############
###############################################################

####################### Formulario de Resolucion ##############
class ResolucionListview(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ('erpbd.view_auditorias_diarias', 'erpbd.change_auditorias_diarias')
    model = auditorias_diarias
    template_name = 'auditoria/resolucion_list.html'
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return auditorias_diarias.objects.filter(container_stat_dsc='Closed').exclude(auditor_id = 'No Asign').order_by('-last_change_ts')[:1000]
    def get_context_data(self, **kwargs): # -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Auditorias Asignadas'
        context['list_url'] = reverse_lazy('resolucion_list')
        context['entity'] = reverse_lazy('resolucion_list')
        success_url = reverse_lazy('resolucion_list')
        return context

class ResolucionUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = ('erpbd.view_auditorias_diarias', 'erpbd.change_auditorias_diarias')
    model = auditorias_diarias
    form_class = UpdateResolucionForm
    template_name = 'auditoria/create.html'
    success_url = reverse_lazy('resolucion_list')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Resolución de Auditorias'
        context['entity'] = 'resolucion_list'
        context['list_url'] = reverse_lazy('resolucion_list')
        success_url = reverse_lazy('resolucion_list')
        context['action'] = 'edit'
        return context

####################### Formulario de Resolucion ##############
###############################################################
#def buscaritem(request):
#    if request.GET["item"]:
#            item = request.GET["item"]
#            if len(item) > 6:
#                print("No Aplica,if")
#                return render(request, 'auditoria/list.html')
#            if len(item) == 0:
#                print("No Aplica,if 2")
#                return render(request, 'auditoria/list.html')
#            else:
#                item_for = request.GET["item"]
#                item_bd = auditorias_diarias.objects.filter(item_nbr=item_for)
#                return render(request, 'auditoria/list.html', {"item_bd": item_bd, "query": item_for})
#    else:
#        return render(request, 'auditoria/list.html')

# export a excel
def export_csv_audit(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = auditorias' + \
                                      str(datetime.now().strftime('%Y-%m-%d %H:%M')) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['auditor_id','supervisor_id_id','container_tag_id', 'container_stat_dsc', 'trip_create_date', 'location_id',
                     'item_nbr','item1_desc','create_ts','last_change_ts'])

    auditorias = auditorias_diarias.objects.filter(container_stat_dsc='Closed').order_by('-last_change_ts')[:1000]

    for audit in auditorias:
        writer.writerow([audit.auditor_id,audit.supervisor_id_id
                        , audit.container_tag_id + '_', audit.container_stat_dsc
                        ,audit.trip_create_date.strftime('%Y-%m-%d %H:%M'),audit.location_id
                        ,audit.item_nbr , audit.item1_desc
                        ,audit.create_ts.strftime('%Y-%m-%d %H:%M')
                        ,audit.last_change_ts.strftime('%Y-%m-%d %H:%M')
                         ])

    return response