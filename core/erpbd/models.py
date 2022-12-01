from django.db import models
from django.contrib.auth.models import User, Group

from crum import get_current_user
import datetime
from datetime import datetime
from django.contrib import auth
from django.conf import settings
# para signals
from django.db.models.signals import post_save , post_delete
from django.dispatch import receiver
# Create your models here.
from core.models import BaseModel


class resolucion_auditoria(models.Model):
    obs_auditoria_cd = models.CharField(max_length=30,default='Ninguno')
    usuario = models.CharField(max_length=20)
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.obs_auditoria_cd

    class Meta():
        verbose_name = 'resolucion auditoria'
        verbose_name_plural = 'resolucion auditorias'
        db_table = 'resolucion_auditoria'
        ordering = ['-fecha_modificacion']


class Estado_Auditoria(models.Model):
    estado_desc = models.CharField(max_length=30,default='Ninguno')
    usuario = models.CharField(max_length=20)
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.estado_desc

    class Meta():
        verbose_name = 'estado auditoria'
        verbose_name_plural = 'estados auditorias'
        db_table = 'estado_auditoria'
        ordering = ['-fecha_modificacion']


class auditorias_diarias(BaseModel):
    user = [('j0c0af6', 'j0c0af6'),
            ('v0j0af6', 'v0j0af6'),
            ('C0j0a56', 'C0j0a56'),
            ('Z0j0a30', 'Z0j0a30'),]

    dc_nbr=models.CharField(max_length=10)
    parent_container_tag_id=models.CharField(max_length=20)
    container_id = models.CharField(max_length=10, verbose_name='container_id')
    container_tag_id =models.CharField(max_length=20,verbose_name = "container_tag_id")
    container_stat_cd=models.IntegerField()
    container_stat_dsc=models.CharField(max_length=25)
    cntnr_type_code=models.IntegerField()
    cntnr_type_desc=models.CharField(max_length=25)
    parent_cntnr_id=models.CharField(max_length=8)
    trip_create_date=models.DateTimeField()
    label_format_code=models.IntegerField()
    label_format_desc=models.CharField(max_length=45)
    last_change_userid=models.CharField(max_length=10)
    last_change_ts=models.DateTimeField(auto_now=True, auto_now_add=True)
    location_id=models.CharField(max_length=14)
    dest_store_nbr=models.CharField(max_length=3)
    dc_sel_section_id=models.CharField(null=True,max_length=6)
    label_create_ts=models.DateTimeField()
    item_nbr=models.CharField(max_length=6)
    item1_desc=models.CharField(max_length=20)
    dpto_name=models.CharField(max_length=30)
    ship_unit_qty=models.IntegerField()
    ship_unit_stat_cd=models.IntegerField()
    shipunit_stat_desc=models.CharField(max_length=30)
    cur_loc_slot_id=models.CharField(max_length=11)
    last_change_ts=models.DateTimeField(auto_now=True)
    create_ts=models.DateTimeField()
    auditor_id = models.CharField(max_length=8, choices=user, verbose_name="Auditor", default='No Asign')
    resolucion_cd = models.ForeignKey(Estado_Auditoria,on_delete=models.CASCADE)
    obs_auditoria_cd = models.ForeignKey(resolucion_auditoria,on_delete=models.CASCADE)
    fecha_Asignacion = models.DateTimeField(auto_now=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        usuario = get_current_user()
        grupo = User.objects.get(username=usuario)
        grupo = str(grupo.groups.get())

        if not self.pk and grupo == 'supervisor':
            self.supervisor_id = usuario
        elif grupo == 'sa':
            self.supervisor_id = usuario
        elif grupo == 'supervisor':
            self.supervisor_id = usuario
        else:
            print('aplico else')
        super(auditorias_diarias, self).save()

    class Meta():
        verbose_name = 'auditoria diaria'
        verbose_name_plural = 'auditorias diarias'
        db_table = 'auditorias_diarias'
        ordering = ['-create_ts']


class auditorias_diarias_log(models.Model):
    usuario = models.CharField(max_length=8,null=True)
    container_tag_id = models.CharField(max_length=20,null=True, verbose_name="container_tag_id")
    last_change_ts = models.DateTimeField(null=True)

    class Meta():
        verbose_name = 'auditoria diaria log'
        verbose_name_plural = 'auditorias diarias log'
        db_table = 'auditorias_diarias_log'
        ordering = ['-last_change_ts']


@receiver(post_save,sender = auditorias_diarias)
def audi_diarias_guardar(sender, instance, **kwargs):
    etiqueta = instance.container_tag_id
    usuario = instance.user


class auditorias(models.Model):
    #verbose_name permite cambiar el nombre en el panel admin
    container_tag_id = models.CharField(primary_key=True,max_length=21,verbose_name="Etiqueta DCL")
    item_nbr = models.CharField(max_length=7)
    user_audit_code = models.CharField(max_length=10)
    fecha_asignacion = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Asignación')
    def __str__(self):
        return self.item_nbr

    class Meta():
        verbose_name = 'auditoria'
        verbose_name_plural = 'auditorias'
        db_table = 'auditorias'
        ordering = ['-fecha_asignacion']

class asignaciones(models.Model):
    container_tag_id = models.CharField(primary_key=True,max_length=21,default= '000000000000000000',verbose_name='etiqueta')
    user_audit_code = models.CharField(max_length=10,null=True,blank=True)
    user_supervisor_code = models.CharField(max_length=10,null=True,blank=True)
    fecha_asignacion = models.DateTimeField(auto_now = True,verbose_name = "Fecha Asignación")
    container_stat_cd = models.IntegerField(default= '15')
    create_ts = models.DateTimeField(auto_now = True,verbose_name = "Fecha Creación Etiqueta")
    class Meta():
        verbose_name = 'asignacion'
        verbose_name_plural = 'asignaciones'
        db_table = 'asignaciones'
        ordering = ['-fecha_asignacion']
