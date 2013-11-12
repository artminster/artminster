from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.views.generic.simple import redirect_to

# Base URL patterns for AppName
from views import Index, ModelNameDetail, ModelNameCreate, ModelNameUpdate, ModelNameDelete
urlpatterns = patterns('',
	url(r'add/$', ModelNameCreate.as_view(), name='modelname_add'),
	url(r'(?P<pk>\d+)/edit/$', ModelNameUpdate.as_view(), name='modelname_update'),
	url(r'(?P<pk>\d+)/delete/$', ModelNameDelete.as_view(), name='modelname_delete'),
	url(r'^(?P<slug>[-\w]+)/$', ModelNameDetail.as_view(), name='modelname_detail'),
	url(r"^$", Index.as_view(),  name="modelname_index"),
)