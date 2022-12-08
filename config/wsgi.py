"""
WSGI config for appauditoria project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings_module = 'quickstartproject.production' if 'auditoria-wm' in os.environ else 'auditoria-wm'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
