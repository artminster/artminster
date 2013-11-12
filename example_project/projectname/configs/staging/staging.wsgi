import os, sys

# put the Django project on sys.path
sys.path.append('/home/artminster/sites/projectname/repository')
sys.path.append('/home/artminster/sites/projectname/repository/allauth')
sys.path.append('/home/artminster/sites/projectname/repository/projectname')

os.environ["DJANGO_SETTINGS_MODULE"] = "projectname.configs.staging.settings"

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()