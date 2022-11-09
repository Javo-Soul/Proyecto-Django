from django.urls import path
from core.erpbd.views.auditoria.views import *
from core.erpbd.views.dashboard import views
from core.erpbd.views.auditoria import views
from core.erpbd.views.dashboard.views import *

urlpatterns =[
    #Supervisor
    path('auditoria/list', Auditoriasdiariaslistview.as_view(), name='auditorias'),
    path('auditoria/add', AuditoriasdiariasCreateView.as_view(), name='auditorias_create'),
    path('auditoria/edit/<str:pk>', AsignacionesUpdateView.as_view(), name='auditorias_update'),

    #Auditor
    path('auditoria/resolucionelist', ResolucionListview.as_view(), name='resolucion_list'),
    path('auditoria/resolucionupdate/<str:pk>', ResolucionUpdateView.as_view(), name='resolucion_update'),

    # Analista/supervisor
    path('auditoria/dashboard', DashboardView.as_view(), name='dashboard'),

    path('export_csv', views.export_csv_audit, name='export-csv'),

    path('auditoria/dashboard/Auditoria Recepcion', DashboardRecepcionView.as_view(), name='auditoriarecep'),
    path('auditoria/dashboard/Auditoria Preparado', DashboardPreparadoView.as_view(), name='auditoriaprepa'),
    path('auditoria/dashboard/Auditoria Despacho',DashboardDespachoView.as_view(), name='auditoriadespa'),
]