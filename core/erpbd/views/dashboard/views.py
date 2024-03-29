from multiprocessing import context
from pkgutil import get_data
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.views.generic import ListView, UpdateView, TemplateView
from django.db.models.functions import TruncMonth, TruncDate , Cast ,Coalesce
from django.db.models.fields import DateField
from django.db.models import Avg, Sum, Max, Min, Count
from django.http import HttpResponse

from core.erpbd.models import auditorias_diarias, asignaciones
import datetime
from datetime import datetime

# Create your views here.
class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    #datos = [pallet=0,cajas=0]
    # pallet_pendientes = 0
    # pallet_asignados = 0
    # cnt_closed = 0
    # cnt_combined = 0
    # cnt_Awaiting_Orderfill = 0
    # todo = 0

    dias_auditorias = auditorias_diarias.objects.dates('trip_create_date','day')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_dias_auditorias(self):
        date_auditorias = auditorias_diarias.objects.dates('trip_create_date', 'day')
        date_audi = []

        for i in range(len(date_auditorias)):
            dias = date_auditorias[i].strftime('%Y-%m-%d')
            date_audi.append(dias)

        return str(date_audi)

    def get_pallet_diarias(self):
        mes = datetime.now().month
        dias = self.dias_auditorias
        pallet = []
        for i in range(len(dias)):
            total = auditorias_diarias.objects.filter(container_stat_dsc='Closed',trip_create_date__date=dias[i]).aggregate(
                r=Coalesce(Count('container_id', distinct=True), 0)).get('r')
            pallet.append(total)
        #print('esto es pallet ', pallet)
        return pallet

    def get_asignaciones_diarias(self):
        dias = self.dias_auditorias
        asignacion = []
        for i in range(len(dias)):
            total = auditorias_diarias.objects.filter(container_stat_dsc='Closed',label_create_ts__date=dias[i]).exclude(auditor_id = 'No Asign').aggregate(
                r=Coalesce(Count('container_id', distinct=True), 0)).get('r')
            asignacion.append(total)

        #print('esto es asignacion ', asignacion)
        return asignacion

    def cajas(self):
        cajas = auditorias_diarias.objects.filter(container_stat_dsc='Closed').aggregate(cajas=Sum('ship_unit_qty'))
        cajas = cajas['cajas']
        return cajas

    def pallet(self):
        pallet = auditorias_diarias.objects.filter(container_stat_dsc='Closed').aggregate(pallet=Count('container_id'))
        pallet = pallet['pallet']
        return pallet

    def pallet_asignados(self):
        pallet_asignados = auditorias_diarias.objects.filter(container_stat_dsc='Closed').exclude(auditor_id='No Asign').count()
        return pallet_asignados

    def pallet_pendientes(self):
        pallet_pendientes = auditorias_diarias.objects.filter(container_stat_dsc='Closed',auditor_id='No Asign').count()
        return pallet_pendientes

    def cnt_closed(self):
        cnt_closed = auditorias_diarias.objects.filter(container_stat_dsc='Closed').values('container_id').count()  
        return cnt_closed

    def cnt_combined(self):
        cnt_combined = auditorias_diarias.objects.filter(container_stat_dsc='Combined').values('container_id').count()
        return cnt_combined

    def cnt_Awaiting_Orderfill(self):
        cnt_Awaiting_Orderfill = auditorias_diarias.objects.filter(container_stat_dsc='Awaiting Orderfill').values('container_id').count()
        return cnt_Awaiting_Orderfill

    def todo(self):
        todo = auditorias_diarias.objects.all()[0:50]
        return todo


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['dias_auditorias'] = self.get_dias_auditorias()
        context['cajas_totales'] = self.cajas()
        context['pallet_totales'] = self.pallet()
        context['pallet_asignados'] = self.pallet_asignados()
        context['pallet_pendientes'] = self.pallet_pendientes()
        context['graph_asignacion_diaria'] = self.get_asignaciones_diarias()
        context['graph_pallet_diarios'] = self.get_pallet_diarias()
        context['cnt_closed'] = self.cnt_closed()
        context['cnt_combined'] = self.cnt_combined()
        context['cnt_Awaiting_Orderfill'] = self.cnt_Awaiting_Orderfill()
        context['todo'] = self.todo()
        return context

class DashboardRecepcionView(TemplateView):
    template_name = 'auditoria/resumen.html'
    datos = 0
    pallet_pendientes = 0
    cnt_closed = 0
    cnt_combined = 0
    cnt_Awaiting_Orderfill = 0
    todo = 0

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_cajas_diarias(self):
        year = datetime.now().year
        dia = datetime.now().date
        cajas=[]
        try:
            for m in range(1, 30):
                total = auditorias_diarias.objects.filter(label_create_ts__day=m, label_create_ts__year=year).aggregate(
                    r=Coalesce(Sum('ship_unit_qty'), )).get('r')
                cajas.append(total)
        except:
            pass
        return cajas

    def get_pallet_diarias(self):
        year = datetime.now().year
        dia = datetime.now().date
        pallet=[]
        try:
            for m in range(1, 30):
                total = auditorias_diarias.objects.filter(label_create_ts__day=m, label_create_ts__year=year).aggregate(
                    r=Coalesce(Count('container_id', distinct=True), )).get('r')
                pallet.append(total)
        except:
            pass
        return pallet


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard Recepción'
        context['cajas_totales'] = self.datos['cajas']
        context['pallet_totales'] = self.datos['pallet']
        context['pallet_pendientes'] = self.pallet_pendientes
        context['graph_cajas_diarias'] = self.get_cajas_diarias()
        context['graph_pallet_diarios'] = self.get_pallet_diarias()
        context['cnt_closed'] = self.cnt_closed
        context['cnt_combined'] = self.cnt_combined
        context['cnt_Awaiting_Orderfill'] = self.cnt_Awaiting_Orderfill

        context['todo'] = self.todo
        return context

class DashboardPreparadoView(TemplateView):
    template_name = 'auditoria/resumen.html'
    datos = 0
    pallet_pendientes = 0
    cnt_closed = 0
    cnt_combined = 0
    cnt_Awaiting_Orderfill = 0
    todo = 0

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_cajas_diarias(self):
        year = datetime.now().year
        dia = datetime.now().date
        cajas=[]
        try:
            for m in range(1, 30):
                total = auditorias_diarias.objects.filter(label_create_ts__day=m, label_create_ts__year=year).aggregate(
                    r=Coalesce(Sum('ship_unit_qty'), 0)).get('r')
                cajas.append(total)
        except:
            pass
        return cajas

    def get_pallet_diarias(self):
        year = datetime.now().year
        dia = datetime.now().date
        pallet=[]
        try:
            for m in range(1, 30):
                total = auditorias_diarias.objects.filter(label_create_ts__day=m, label_create_ts__year=year).aggregate(
                    r=Coalesce(Count('container_id', distinct=True), 0)).get('r')
                pallet.append(total)
        except:
            pass
        return pallet


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard Preparado'
        context['cajas_totales'] = self.datos['cajas']
        context['pallet_totales'] = self.datos['pallet']
        context['pallet_pendientes'] = self.pallet_pendientes
        context['graph_cajas_diarias'] = self.get_cajas_diarias()
        context['graph_pallet_diarios'] = self.get_pallet_diarias()
        context['cnt_closed'] = self.cnt_closed
        context['cnt_combined'] = self.cnt_combined
        context['cnt_Awaiting_Orderfill'] = self.cnt_Awaiting_Orderfill

        context['todo'] = self.todo
        return context

class DashboardDespachoView(TemplateView):
    template_name = 'auditoria/resumen.html'
    datos = 0
    pallet_pendientes = 0
    cnt_closed = 0
    cnt_combined = 0
    cnt_Awaiting_Orderfill = 0
    todo = 0

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_cajas_diarias(self):
        year = datetime.now().year
        dia = datetime.now().date
        cajas=[]
        try:
            for m in range(1, 30):
                total = auditorias_diarias.objects.filter(label_create_ts__day=m, label_create_ts__year=year).aggregate(
                    r=Coalesce(Sum('ship_unit_qty'), 0)).get('r')
                cajas.append(total)
        except:
            pass
        return cajas

    def get_pallet_diarias(self):
        year = datetime.now().year
        dia = datetime.now().date
        pallet=[]
        try:
            for m in range(1, 30):
                total = auditorias_diarias.objects.filter(label_create_ts__day=m, label_create_ts__year=year).aggregate(
                    r=Coalesce(Count('container_id', distinct=True), 0)).get('r')
                pallet.append(total)
        except:
            pass
        return pallet


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard Despacho'
        context['cajas_totales'] = self.datos['cajas']
        context['pallet_totales'] = self.datos['pallet']
        context['pallet_pendientes'] = self.pallet_pendientes
        context['graph_cajas_diarias'] = self.get_cajas_diarias()
        context['graph_pallet_diarios'] = self.get_pallet_diarias()
        context['cnt_closed'] = self.cnt_closed
        context['cnt_combined'] = self.cnt_combined
        context['cnt_Awaiting_Orderfill'] = self.cnt_Awaiting_Orderfill

        context['todo'] = self.todo
        return context
