import os, django, urllib
from artminster.core.settings import *
from artminster.core.utils.settings_utils import remove_duplicates

# CORE SETTINGS
###########################################################################################
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

STATIC_ROOT = os.path.join(SITE_ROOT, "static")
ADMIN_MEDIA_PREFIX = "/static/admin/"
MEDIA_ROOT = os.path.join(SITE_ROOT, "media")

SECRET_KEY = '-x83)5-^cugn@*t6gh%76j@cb)zj)q7l_rm!%3=)@sw&v&d_ww'

ADMINS = (('ARTMINSTER Dev', 'dev@artminster.com')),
MANAGERS = ('ARTMINSTER Dev', 'dev@artminster.com'),

PROJECT_SITE_NAME = 'projectname'
CONTACT_EMAIL = "info@projectname.com"
PROJECT_DOMAIN = "http://127.0.0.1:8000"
DEFAULT_PROFILE_IMAGE = os.path.join(MEDIA_ROOT, 'uploads/projectname_defaults/profile_portrait_default.png')

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'projectname',
		'USER': 'projectname',
		'PASSWORD': 'projectname',
		'HOST': 'localhost',
	}
}

if 'apps.myshop' in INSTALLED_APPS:
	from apps.myshop.settings import SHOP_INSTALLED_APPS
	INSTALLED_APPS += SHOP_INSTALLED_APPS

INSTALLED_APPS += (
	# Local Project Apps
	'apps.projectname_profile',
	'apps.projectname',
)
DISABLED_APPS = ()

DISABLED_MIDDLEWARE_CLASSES = ()

TEMPLATE_DIRS = (
	os.path.join(SITE_ROOT, 'templates'),
)

ROOT_URLCONF = 'projectname.configs.common.urls'
AUTH_PROFILE_MODULE = 'projectname_profile.UserProfile'


# GOOGLE API & ANALYTICS SETTINGS
###########################################################################################
GOOGLE_ANALYTICS_CODE = None
GOOGLE_MAPS_API_KEY = "AIzaSyBg7rZjToQyi9izk13QfLegTueVEuWxfa0"


# CACHE SETTINGS
###########################################################################################
CACHE_MIDDLEWARE_KEY_PREFIX='projectname:'
CACHE_PREFIX = "projectname:"
CMS_CACHE_PREFIX = "cms_projectname:"
JOHNNY_MIDDLEWARE_KEY_PREFIX='jc_projectname'


# ADMIN MODIFICATION SETTINGS
###########################################################################################
ADMIN_SHORTCUTS = [
	{
		'shortcuts': [
			{
				'url': '/',
				'open_new_window': True,
			},
			{
				'url_name': 'admin:cms_page_changelist',
				'title': 'Pages',
			},
			{
				'url': '/admin/filebrowser/browse/',
				'title': 'Files',
				'class': 'folder'
			},
			{
				'url_name': 'admin:auth_user_changelist',
				'title': 'Users',
			},
		]
	},
]
ADMIN_SHORTCUTS_SETTINGS = {
	'hide_app_list': True,
	'open_new_window': False,
}


# FILEBROWSER SETTINGS
###########################################################################################
FILEBROWSER_VERSIONS = {
	'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'},
	'thumb': {'verbose_name': 'Grid Thumb', 'width': 150, 'height': 150, 'opts': 'crop upscale'},
	'small': {'verbose_name': 'Small (210px)', 'width': 210, 'height': '', 'opts': ''},
	'medium': {'verbose_name': 'Medium (370px)', 'width': 370, 'height': '', 'opts': ''},
	'large': {'verbose_name': 'Large (530px)', 'width': 530, 'height': '', 'opts': ''},

	'box-image-list-item': { 'width': 75, 'height': 41, 'opts': 'crop upscale' },
	'box-main-image-list-item': { 'width': 124, 'height': 93, 'opts': 'crop upscale' },
}
FILEBROWSER_ADMIN_VERSIONS = [
	'thumb', 'small','medium','large',
]


# DJANGO CMS SETTINGS
###########################################################################################
CMS_TEMPLATES = (
	('cms/standard_page.html', 'Standard Page'),
)


# DJANGO STATIC SETTINGS
###########################################################################################
DJANGO_STATIC = not DEBUG
DJANGO_STATIC_SAVE_PREFIX = os.path.join(MEDIA_ROOT, 'cache-forever')
DJANGO_STATIC_NAME_PREFIX = "cache-forever/"
if DEBUG:
	DJANGO_STATIC_MEDIA_URL = STATIC_URL
else:
	DJANGO_STATIC_MEDIA_URL = MEDIA_URL
DJANGO_STATIC_MEDIA_URL_ALWAYS = True
DJANGO_STATIC_MEDIA_ROOTS = [os.path.join(SITE_ROOT, 'apps/common/static'), STATIC_ROOT, MEDIA_ROOT]


# PER APP / DEVELOPER SETTINGS IMPORTS
###########################################################################################
from auth_settings import *

INSTALLED_APPS = remove_duplicates(INSTALLED_APPS)
if 'DISABLED_APPS' in locals():
	INSTALLED_APPS = [k for k in INSTALLED_APPS if k not in DISABLED_APPS]

if 'DISABLED_MIDDLEWARE_CLASSES' in locals():
	INSTALLED_APPS = [k for k in INSTALLED_APPS if k not in DISABLED_MIDDLEWARE_CLASSES]

if 'apps.myshop' in INSTALLED_APPS:
	from apps.myshop.settings import *
	INSTALLED_APPS += SHOP_INSTALLED_APPS
	ADMIN_SHORTCUTS += SHOP_ADMIN_SHORTCUTS

try:
	from local_settings import *
except ImportError:
	pass
