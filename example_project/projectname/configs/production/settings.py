from projectname.configs.common.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
PROJECT_DOMAIN = "http://projectname.com"

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'projectname',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
    }
}

# Caching
CACHE_BACKEND = 'johnny.backends.memcached://127.0.0.1:11211'
GOOGLE_MAPS_API_KEY = "AIzaSyBg7rZjToQyi9izk13QfLegTueVEuWxfa0"

ADMINS = (('ARTMINSTER Dev', 'dev@artminster.com')),
MANAGERS = ('ARTMINSTER Dev', 'dev@artminster.com'),

PAYPAL_RECEIVER_EMAIL = ""
PAYPAL_SANDBOX_MODE = False