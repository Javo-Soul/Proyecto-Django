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
    datos = auditorias_diarias.objects.filter(container_stat_dsc='Closed').aggregate(pallet=Count('container_id'),
                                                                                     cajas=Sum('ship_unit_qty'))
    pallet_pendientes = auditorias_diarias.objects.filter(container_stat_dsc='Closed',user='No Asign').count()
    pallet_asignados = auditorias_diarias.objects.filter(container_stat_dsc='Closed').exclude(user='No Asign').count()
    cnt_closed = auditorias_diarias.objects.filter(container_stat_dsc='Closed').values('container_id').count()
    cnt_combined = auditorias_diarias.objects.filter(container_stat_dsc='Combined').values('container_id').count()
    cnt_Awaiting_Orderfill = auditorias_diarias.objects.filter(container_stat_dsc='Awaiting Orderfill').values('container_id').count()
    todo = auditorias_diarias.objects.all()[0:50]
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
        #dias = auditorias_diarias.objects.annotate(Fecha_etiqueta = TruncDate('trip_create_date')).values('Fecha_etiqueta').annotate(cantidad = Count('container_id')).order_by('trip_create_date')
        #dias = auditorias_diarias.objects.values('trip_create_date__date').annotate(count = Count('container_id')).values('trip_create_date__date').order_by('trip_create_date__date')
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
            total = auditorias_diarias.objects.filter(container_stat_dsc='Closed',label_create_ts__date=dias[i]).exclude(user = 'No Asign').aggregate(
                r=Coalesce(Count('container_id', distinct=True), 0)).get('r')
            asignacion.append(total)

        #print('esto es asignacion ', asignacion)
        return asignacion


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['dias_auditorias'] = self.get_dias_auditorias()
        context['cajas_totales'] = self.datos['cajas']
        context['pallet_totales'] = self.datos['pallet']
        context['pallet_asignados'] = self.pallet_asignados
        context['pallet_pendientes'] = self.pallet_pendientes
        context['graph_asignacion_diaria'] = self.get_asignaciones_diarias()
        context['graph_pallet_diarios'] = self.get_pallet_diarias()
        context['cnt_closed'] = self.cnt_closed
        context['cnt_combined'] = self.cnt_combined
        context['cnt_Awaiting_Orderfill'] = self.cnt_Awaiting_Orderfill
        context['todo'] = self.todo
        return context

class DashboardRecepcionView(TemplateView):
    template_name = 'auditoria/resumen.html'
    datos = auditorias_diarias.objects.filter(container_stat_dsc='Closed').aggregate(pallet=Count('container_id', distinct=True),
                                                                                     cajas=Sum('ship_unit_qty'))
    pallet_pendientes = asignaciones.objects.filter(user_audit_code='').count()
    cnt_closed = auditorias_diarias.objects.filter(container_stat_dsc='Closed').values('container_id').distinct().count()
    cnt_combined = 0
    cnt_Awaiting_Orderfill = auditorias_diarias.objects.filter(container_stat_dsc='Awaiting Orderfill').values('container_id').distinct().count()
    todo = auditorias_diarias.objects.all()[0:50]

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
    datos = auditorias_diarias.objects.filter(container_stat_dsc='Closed').aggregate(pallet=Count('container_id', distinct=True),
                                                                                     cajas=Sum('ship_unit_qty'))
    pallet_pendientes = asignaciones.objects.filter(user_audit_code='').count()
    cnt_closed = auditorias_diarias.objects.filter(container_stat_dsc='Closed').values('container_id').distinct().count()
    cnt_combined = auditorias_diarias.objects.filter(container_stat_dsc='Combined').values('container_id').distinct().count()
    cnt_Awaiting_Orderfill = auditorias_diarias.objects.filter(container_stat_dsc='Awaiting Orderfill').values('container_id').distinct().count()
    todo = auditorias_diarias.objects.all()[0:50]

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
    datos = auditorias_diarias.objects.filter(container_stat_dsc='Closed').aggregate(pallet=Count('container_id', distinct=True),
                                                                                     cajas=Sum('ship_unit_qty'))
    pallet_pendientes = asignaciones.objects.filter(user_audit_code='').count()
    cnt_closed = auditorias_diarias.objects.filter(container_stat_dsc='Closed').values('container_id').distinct().count()
    cnt_combined = auditorias_diarias.objects.filter(container_stat_dsc='Combined').values('container_id').distinct().count()
    cnt_Awaiting_Orderfill = auditorias_diarias.objects.filter(container_stat_dsc='Awaiting Orderfill').values('container_id').distinct().count()
    todo = auditorias_diarias.objects.all()[0:50]

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
