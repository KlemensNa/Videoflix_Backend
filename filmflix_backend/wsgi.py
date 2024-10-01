"""
WSGI config for filmflix_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'filmflix_backend.settings')

application = get_wsgi_application()


# import os
# import sys

# path = '/home/hamishwillee/hamishwillee.pythonanywhere.com'
# if path not in sys.path:
#     sys.path.append(path)

# os.environ['DJANGO_SETTINGS_MODULE'] = 'locallibrary.settings'

# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
