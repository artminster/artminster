import os, sys

# put the Django project on sys.path
sys.path.append('/home/artminster/sites/artminster/repository')
sys.path.append('/home/artminster/sites/artminster/repository/allauth')
sys.path.append('/home/artminster/sites/artminster/repository/artminster')


os.environ["DJANGO_SETTINGS_MODULE"] = "artminster.configs.production.settings"

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()