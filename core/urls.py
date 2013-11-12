from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#from django.views.generic.simple import redirect_to
from django.views.generic import RedirectView

import os

handler500 = 'artminster.core.views.server_error'
admin.autodiscover()

try:
	from filebrowser.sites import site
except:
	pass

# Internal app patterns
urlpatterns = patterns('',
	url(r'^accounts/', include('artminster.core.apps.profile.urls')),
)

# Admin patterns
urlpatterns += patterns('',
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
	#(r'^grappelli/', include('grappelli.urls')),
)

try:
	urlpatterns += patterns('', (r'^admin/filebrowser/', include(site.urls)),)
except:
	urlpatterns += patterns('', (r'^admin/filebrowser/', include('filebrowser.urls')),)

# Site media patterns
urlpatterns += patterns('',
	(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
	(r'^apple\-touch\-icon\.png$', RedirectView.as_view(url='/static/img/apple-touch-icon.png')),
	(r'^robots\.txt$', RedirectView.as_view(url='/static/robots.txt')),
	#(r'^favicon\.ico$', redirect_to, {'url': '/static/img/favicon.ico'}),
	#(r'^apple\-touch\-icon\.png$', redirect_to, {'url': '/static/img/apple-touch-icon.png'}),
	#(r'^robots\.txt$', redirect_to, {'url': '/static/robots.txt'}),
	(r'^tinymce/', include('tinymce.urls')),
	(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
	(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages':'django.conf'}),
)

if settings.DEBUG:
	urlpatterns+= patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
			'document_root': settings.MEDIA_ROOT
		}),
		(r'^cache-forever/(?P<path>.*)$', 'django.views.static.serve', {
			'document_root': settings.STATIC_ROOT,
		}),
		(r'^404/$', 'django.views.defaults.page_not_found'),
		(r'^500/$', 'artminster.core.views.server_error'),
	)

# Pluggable apps
urlpatterns += patterns('',
	url(r'^accounts/', include('allauth.urls')),
	url(r'^', include('cms.urls')),
)

urlpatterns += staticfiles_urlpatterns()
