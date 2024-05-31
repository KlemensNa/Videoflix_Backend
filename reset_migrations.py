import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "filmflix_backend.settings")
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DELETE FROM django_migrations WHERE app='admin';")
    cursor.execute("DELETE FROM django_migrations WHERE app='filmflix';")
    print("Migrationseinträge gelöscht.")