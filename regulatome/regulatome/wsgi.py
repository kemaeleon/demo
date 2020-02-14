"""
WSGI config for regulatome project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys, site
sys.path.append('/var/www/regulatome/admindir/regulatome_env/lib/python3.5/site-packages/')
sys.path.append('/var/www/regulatome/docroot/regulatome-repo/regulatome/')

import django
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'regulatome.settings')
application = get_wsgi_application()
