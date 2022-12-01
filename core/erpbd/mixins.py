from django.shortcuts import redirect
from django.contrib import auth
from crum import get_current_user

class IsSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = auth.get_user(request)
        group = str(request.user.groups.values_list('name', flat=True).first())
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        elif group == 'supervisor':
            return super().dispatch(request, *args, **kwargs)

        elif group == 'auditor':
            return redirect('auditorias')

        return redirect('dashboard')


class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            print('Aplico superuser')
            return super().dispatch(request, *args, **kwargs)
        return redirect('dashboard')