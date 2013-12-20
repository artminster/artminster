from django.contrib.messages import constants as message_constants
import os, django, urllib

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# Debugging
DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (('ARTMINSTER Dev', 'dev@artminster.com'),)
MANAGERS = ADMINS

# Local time
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-GB'
SITE_ID = 1
USE_I18N = False
DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    "allauth.account.auth_backends.AuthenticationBackend",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "artminster.core.utils.context_processors.app_wide_vars",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
    'pagination.middleware.PaginationMiddleware',
    #'slimmer.middleware.CompressHtmlMiddleware',
    #'cms.middleware.multilingual.MultilingualURLMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
]
TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = [
    # Base Django Apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'grappelli.dashboard',
    #'grappelli',
    'djangocms_admin_style',
    'admin_shortcuts',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.markup',
    'django.contrib.sitemaps',
    'django.contrib.humanize',

    # Utilities & Helper Apps
    'artminster.core',
    #'artminster.core.apps.profile',
    'tinymce',
    'south',
    'filebrowser',
    'django_extensions',
    'django_static',
    'johnny',
    'pagination',
    'djangular',

    # Registration, Signin and Account Management
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.openid',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',
    #'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.soundcloud',

    # Django CMS
    'cms',
    'mptt',
    'menus',

    # Django CMS Plugins
    'cms.plugins.text',
    'cms.plugins.picture',
    'cms.plugins.file',
    'cms.plugins.link',
    'cms.plugins.snippet',
    'cms.plugins.flash',
    'cms.plugins.googlemap',
    'cms.plugins.teaser',
    'cms.plugins.video',
    'cms.plugins.twitter',
    'sekizai',
]

if DEBUG:
    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.debug',)
    #MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    #INSTALLED_APPS += ('debug_toolbar',)

if USE_I18N:
    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.i18n',)

#MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
#MESSAGE_LEVEL = message_constants.DEBUG

# CACHE SETTINGS
CACHE_BACKEND = 'johnny.backends.locmem://'
CACHE_MIDDLEWARE_SECONDS=90 * 60 # 90 minutes
CACHE_COUNT_TIMEOUT = 60

# EMAIL SETTINGS
DEFAULT_FROM_EMAIL = 'noreply@artminster.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@artminster.com'
EMAIL_HOST_PASSWORD = '2M5394'

# Authentication / Account Management Settings
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = "/"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_AVATAR_SUPPORT = False
EMAIL_CONFIRMATION_DAYS = 99
FACEBOOK_ENABLED = True
TWITTER_ENABLED = True
OPENID_ENABLED = False
SOCIALACCOUNT_ENABLED = True
SOCIALACCOUNT_PROVIDERS = {}

# GRAPPELLI SETTINGS
GRAPPELLI_ADMIN_URL = '/admin'
GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

# Django-filebrowser settings
FILEBROWSER_URL_FILEBROWSER_MEDIA = STATIC_URL + "filebrowser/"
FILEBROWSER_PATH_FILEBROWSER_MEDIA = os.path.join(STATIC_URL, 'filebrowser/')
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
    'Video': ['.mov','.wmv','.mpeg','.mpg','.avi','.rm','.swf'],
    'Document': ['.pdf','.doc','.rtf','.txt','.xls','.csv'],
    'Sound': ['.mp3','.mp4','.wav','.aiff','.midi','.m4p'],
    'Code': ['.html','.py','.js','.css'],
    # for TinyMCE we also have to define lower-case items
    'image': ['Image'],
    'file': ['Folder','Image','Document',],
}

FILEBROWSER_ADMIN_THUMBNAIL = 'fb_thumb'
FILEBROWSER_IMAGE_MAXBLOCK = 1024*1024
FILEBROWSER_MAX_UPLOAD_SIZE = 10485760 # 10485760 bytes = about 10megs

# RAWJAM WEBSITE (Used on trademark)
RAWJAM_WEBSITE = 'http://artminster.com/'
RAWJAM_TITLE = 'Creative ideas, brought to life'

# CMS settings
gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
    ('pt', gettext('Portuguese')),
)

CMS_LANGUAGES = {
    1: [
        {
            'code': 'en',
            'name': gettext('English'),
            'fallbacks': [],
            'public': True,
            'hide_untranslated': True,
            'redirect_on_fallback':False,
        },
#        {
#            'code': 'de',
#            'name': gettext('Deutsch'),
#            'fallbacks': ['en', 'fr'],
#            'public': True,
#        },
#        {
#            'code': 'fr',
#            'name': gettext('French'),
#            'public': False,
#        },
    ],
}

CMS_TEMPLATES = (
    ('cms/standard_page.html', 'Standard Page'),
)

CMS_SOFTROOT = True
CMS_MODERATOR = False
CMS_PERMISSION = False
CMS_REDIRECTS = False
CMS_SEO_FIELDS = True
CMS_MENU_TITLE_OVERWRITE = True
CMS_SHOW_END_DATE = True
CMS_SHOW_START_DATE = True
CMS_URL_OVERWRITE = False
CMS_FLAT_URLS = False
CMS_CONTENT_CACHE_DURATION = 60
CMS_USE_TINYMCE = True
CMS_HIDE_UNTRANSLATED = False

CMS_PAGE_MEDIA_PATH = 'uploads/cms_media/'

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

JQUERY_DATEPICKER_DATE_FORMAT = 'yy-mm-dd'

# TINYMCE Configuration

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align' : "center",
    'custom_undo_redo_levels': 10,
    'width': "832",
    'height': "400",
}