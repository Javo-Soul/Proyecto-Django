from django.contrib import admin
from core.erpbd.models import *
# Register your models here.

class AuditoriasAdmin(admin.ModelAdmin):
    list_display= ("container_tag_id","item_nbr","user_audit_code")
    search_fields = ("container_tag_id","item_nbr","user_audit_code")

# con la clase podemos ver la lista en el menu admin
class AsignacionAdmin(admin.ModelAdmin):
    list_display= ("container_tag_id","user_audit_code","user_supervisor_code","fecha_asignacion")
    list_filter =("user_supervisor_code","fecha_asignacion",)
    search_fields = ("user_audit_code","user_supervisor_code",)
    date_hierarchy = ("fecha_asignacion")


class auditorias_diariasAdmin(admin.ModelAdmin):
    #permite ver los campos en forma de tabla
    list_display= ("auditor_id","container_tag_id","container_stat_dsc","cntnr_type_desc","trip_create_date","location_id"
                    ,"item_nbr","item1_desc")
    # Buscador
    search_fields = ("container_tag_id","item_nbr","auditor_id")
    # Filtro
    list_filter =("label_create_ts","item_nbr","auditor_id",)
    # Filtro Fecha
    date_hierarchy = "label_create_ts"

class resolucion_auditoriaAdmin(admin.ModelAdmin):
    #permite ver los campos en forma de tabla
    list_display= ("obs_auditoria_cd","usuario","fecha_modificacion",)
    # Buscador
    search_fields = ("obs_auditoria_cd","usuario")
    # Filtro
    list_filter =("obs_auditoria_cd","usuario",)
    # Filtro Fecha
    date_hierarchy = "fecha_modificacion"

class Estado_AuditoriaAdmin(admin.ModelAdmin):
    #permite ver los campos en forma de tabla
    list_display= ("estado_desc","usuario","fecha_modificacion",)
    # Buscador
    search_fields = ("estado_desc","usuario")
    # Filtro
    list_filter =("estado_desc","usuario",)
    # Filtro Fecha
    date_hierarchy = "fecha_modificacion"


admin.site.register(auditorias,AuditoriasAdmin)
admin.site.register(asignaciones,AsignacionAdmin)
admin.site.register(auditorias_diarias,auditorias_diariasAdmin)
admin.site.register(resolucion_auditoria,resolucion_auditoriaAdmin)
admin.site.register(Estado_Auditoria,Estado_AuditoriaAdmin)
