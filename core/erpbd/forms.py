from datetime import datetime
from django.forms import *
from core.erpbd.models import *


class AuditoriasDiariasForm(ModelForm):
    class Meta:
        model = asignaciones
        fields ='__all__' 
        #['user_audit_code','etiqueta']
        template_name = 'auditoria/create.html'


class AsignacionesForm(ModelForm):
    class Meta:
        model = asignaciones
        fields ='__all__' 
        #['user_audit_code','etiqueta']
        template_name = 'auditoria/create.html'