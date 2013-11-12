from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib import admin

from views import UserProfileDetail, UserProfileUpdate

# Registration/Login views
#urlpatterns = patterns('artminster.core.apps.profile.views.login',
#    url(r"^signup/$", 'signup',  name="account_signup"),
#    url(r"^signin/$", 'signin', name="signin"),
#    url(r"^logout/$", 'logout_view', name="logout"),
#)

urlpatterns = patterns('',
    url(r'^profile/edit/$', UserProfileUpdate.as_view(), {}, name = "edit_profile"),
    url(r'^profile/(?P<username>[\w\-\.\_\@\+]+)/$', UserProfileDetail.as_view(), {}, name = "profile"),
    #url(r'^signup/complete/$', 'register_complete', {}, name = "register_complete"),
)