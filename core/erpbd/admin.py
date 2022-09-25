from django.contrib import admin
from core.erpbd.models import *
# Register your models here.

class AuditoriasAdmin(admin.ModelAdmin):
    list_display= ("etiqueta","item_nbr","user_audit_code")
    search_fields = ("etiqueta","item_nbr","user_audit_code")

# con la clase podemos ver la lista en el menu admin
class AsignacionAdmin(admin.ModelAdmin):
    list_display= ("etiqueta","user_audit_code","user_supervisor_code","fecha_asignacion")
    list_filter =("user_supervisor_code","fecha_asignacion",)
    search_fields = ("user_audit_code","user_supervisor_code",)
    date_hierarchy = ("fecha_asignacion")


class auditorias_diariasAdmin(admin.ModelAdmin):
    #permite ver los campos en forma de tabla
    list_display= ("user","container_tag_id","container_stat_dsc","cntnr_type_desc","trip_create_date","location_id"
                    ,"item_nbr","item1_desc")
    # Buscador
    search_fields = ("container_tag_id","item_nbr","user")
    # Filtro
    list_filter =("label_create_ts","item_nbr","user",)
    # Filtro Fecha
    date_hierarchy = "label_create_ts"


admin.site.register(auditorias,AuditoriasAdmin)
admin.site.register(asignaciones,AsignacionAdmin)
admin.site.register(auditorias_diarias,auditorias_diariasAdmin)

