from django.conf.urls.defaults import *
from django.conf import settings

from cms.sitemaps import CMSSitemap

sitemaps = {
	'cmspages': CMSSitemap
}

# projectname apps
urlpatterns = (
	url(r'^', include('apps.projectname.urls')),
	url(r'^accounts/', include('apps.projectname_profile.urls')),
	url(r'^shop/', include('apps.myshop.urls')),
)

if "artminster.contrib.billing" in settings.INSTALLED_APPS:
	urlpatterns += (
		url(r'^billing/', include('artminster.contrib.billing.urls')),
	)

urlpatterns += (
	url(r'^', include('artminster.core.urls')),
	url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
)
