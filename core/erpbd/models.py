from django.db import models

# Create your models here.

class auditorias(models.Model):
    #verbose_name permite cambiar el nombre en el panel admin
    etiqueta = models.CharField(primary_key=True,max_length=21,verbose_name="Etiqueta DCL")
    item_nbr = models.CharField(max_length=7)
    user_audit_code = models.CharField(max_length=10)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_nbr

    class Meta():
        verbose_name = 'auditoria'
        verbose_name_plural = 'auditorias'
        db_table = 'auditorias'
        ordering = ['-fecha_asignacion']


class asignaciones(models.Model):
    etiqueta = models.CharField(primary_key=True,max_length=21)
    user_audit_code = models.CharField(max_length=10,null=True,blank=True)
    user_supervisor_code = models.CharField(max_length=10,null=True,blank=True)
    fecha_asignacion = models.DateTimeField(auto_now = True,verbose_name = "Fecha Asignación")

    class Meta():
        verbose_name = 'asignacion'
        verbose_name_plural = 'asignaciones'
        db_table = 'asignaciones'
        ordering = ['-fecha_asignacion']


class auditorias_diarias(models.Model):
    dc_nbr=models.CharField(max_length=10)
    user=models.CharField(max_length=8,null=True,blank=True,verbose_name = "Auditor")
    container_id=models.CharField(max_length=9)
    parent_container_tag_id=models.CharField(max_length=20)
    container_tag_id=models.CharField(max_length=20)
    container_stat_cd=models.IntegerField()
    container_stat_dsc=models.CharField(max_length=25)
    cntnr_type_code=models.IntegerField()
    cntnr_type_desc=models.CharField(max_length=25)
    parent_cntnr_id=models.CharField(max_length=8)
    trip_create_date=models.DateTimeField()
    label_format_code=models.IntegerField()
    label_format_desc=models.CharField(max_length=45)
    last_change_userid=models.CharField(max_length=10)
    last_change_ts=models.DateTimeField(auto_now=False, auto_now_add=False)
    location_id=models.CharField(max_length=14)
    dest_store_nbr=models.CharField(max_length=3)
    dc_sel_section_id=models.CharField(null=True,max_length=6)
    label_create_ts=models.DateTimeField()
    shipping_tag_id=models.CharField(primary_key=True,max_length=20)
    rcv_unit_tag_id=models.CharField(max_length=21)
    item_nbr=models.CharField(max_length=6)
    item1_desc=models.CharField(max_length=20)
    dpto_name=models.CharField(max_length=30)
    ship_unit_qty=models.IntegerField()
    ship_unit_stat_cd=models.IntegerField()
    shipunit_stat_desc=models.CharField(max_length=30)
    cur_loc_slot_id=models.CharField(max_length=11)
    last_change_userid=models.CharField(max_length=15)
    last_change_ts=models.DateTimeField(auto_now=True)
    create_ts=models.DateTimeField()

    class Meta():
        verbose_name = 'auditoria diaria'
        verbose_name_plural = 'auditorias diarias'
        db_table = 'auditorias_diarias'
        ordering = ['-create_ts']


