from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.views.generic.simple import redirect_to

# Base URLs
from views import MyAccount
urlpatterns = patterns('',
	url(r"^ipn/5055747087/$", include('paypal.standard.ipn.urls')),
	url(r"^my-account/$", MyAccount.as_view(),  name="my_account"),
)

# Subscription URLs
from views import SubscriptionSignup, SubscriptionComplete, SubscriptionCancel
urlpatterns += patterns('',
	url(r"^subscription/(?P<slug>[-\w]+)/signup/$", SubscriptionSignup.as_view(),  name="subscription_signup"),
	url(r"^subscription/(?P<slug>[-\w]+)/complete/$", SubscriptionComplete.as_view(),  name="subscription_complete"),
	url(r"^subscription/(?P<slug>[-\w]+)/cancel/$", SubscriptionCancel.as_view(),  name="subscription_cancel"),
)

