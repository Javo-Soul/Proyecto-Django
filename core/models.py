from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    supervisor_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_creation',
                                      null=True, blank=True)
    Fecha_creacion_auditoria = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

#user_supervisor_code