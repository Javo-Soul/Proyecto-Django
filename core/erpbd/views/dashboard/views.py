from multiprocessing import context
from pkgutil import get_data
from django.shortcuts import render
from core.erpbd.models import *
from django.views.generic import ListView, UpdateView, TemplateView
from django.db.models import Avg, Sum, Max, Min, Count
from django.http import HttpResponse
from django.db.models.functions import Coalesce
from core.erpbd.models import auditorias_diarias, asignaciones
from datetime import  datetime

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
        context['title'] = 'Dashboard'
        context['cajas_totales'] = self.datos['cajas']
        context['pallet_totales'] = self.datos['pallet']
        context['pallet_asignados'] = self.pallet_asignados
        context['pallet_pendientes'] = self.pallet_pendientes

        context['graph_cajas_diarias'] = self.get_cajas_diarias()
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
    cnt_combined = auditorias_diarias.objects.filter(container_stat_dsc='Combined').values('container_id').distinct().count()
    cnt_Awaiting_Orderfill = auditorias_diarias.objects.filter(container_stat_dsc='Awaiting Orderfill').values('container_id').distinct().count()

    todo = auditorias_diarias.objects.all()[0:50]

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
