from datetime import datetime
from django.forms import *
from core.erpbd.models import *

class AuditoriasDiariasForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = True
        self.fields['etiqueta'].widget.attrs['autofocus'] = True

    class Meta:
        model = asignaciones
        fields ='__all__'#['user_audit_code','etiqueta']
        #template_name = 'auditoria/create.html'
        widget={
            'etiqueta': Textarea(
                attrs= {
                    'placeholder': 'aca',
                }
            ),
        }


class AsignacionesForm(ModelForm):

    class Meta:
        model = asignaciones
        fields ='__all__'
        #
        template_name = 'auditoria/create.html'