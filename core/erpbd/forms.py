from datetime import datetime
from django.forms import *
from core.erpbd.models import *

class AuditoriasDiariasForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = True
        self.fields['container_tag_id'].widget.attrs['autofocus'] = True

        for form in self.visible_fields():
            form.field.widget.attrs['readonly'] = True


    class Meta:
        model = auditorias_diarias
        #'__all__'
        fields =['user','container_tag_id','create_ts'
                 ,'item_nbr','item1_desc','location_id']
        #template_name = 'auditoria/create.html'
        widget={
            'container_tag_id': Textarea(
                attrs= {
                    'placeholder': 'aca',
                }
            ),
        }

class UpdateResolucionForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = True
        self.fields['container_tag_id'].widget.attrs['autofocus'] = True

        for form in self.visible_fields():
            form.field.widget.attrs['readonly'] = True


    class Meta:
        model = auditorias_diarias
        fields = ['container_tag_id', 'create_ts'
            , 'item_nbr', 'item1_desc', 'location_id','resolucion_cd']
        #template_name = 'auditoria/create.html'
        widget={
            'container_tag_id': Textarea(
                attrs= {
                    'placeholder': 'aca',
                }
            ),
        }