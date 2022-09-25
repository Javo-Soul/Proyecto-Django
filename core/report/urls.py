from core.report import views
from django.urls import path
from core.report.views import ReportAuditView

urlpatterns =[
    path('reportaudit/', ReportAuditView.as_view(), name='report_audit'),
]