from core.report.forms import ReportForm
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erpbd.models import *

class ReportAuditView(TemplateView):
    template_name = 'reports/reportaudit.html'
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = auditorias_diarias.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(trip_create_date__range=[start_date, end_date])
                for s in search:
                    data.append([
                        s.container_tag_id,
                        s.container_stat_dsc,
                        s.trip_create_date.strftime('%Y-%m-%d'),
                        s.user,
                        s.user_supervisor_code,
                        s.location_id,
                        s.item_nbr,
                        s.item1_desc,
                        s.create_ts.strftime('%Y-%m-%d'),
                        s.resolucion_cd,
                    ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Auditorias'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('report_audit')
        context['form'] = ReportForm()

        return context

        