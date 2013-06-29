"""
WSGI config for heroject project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os, sys, site

site.addsitedir('/home/ugur/heroject/local/lib/python2.7/site-packages')

from django.core.management import setup_environ
from django.core.wsgi import get_wsgi_application

# Project Added
sys.path.append("/home/ugur/siteler/heroject")

from heroject import settings
setup_environ(settings)
application = get_wsgi_application()
