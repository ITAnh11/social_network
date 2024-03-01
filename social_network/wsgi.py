"""
WSGI config for social_network project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

setting_module = 'social_network.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'social_network.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_module)

application = get_wsgi_application()
