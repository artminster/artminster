import urllib

from django.core.urlresolvers import reverse
from django import http
from django.db.models import Q
from django.template import Context, loader
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage

from allauth.account.views import signup as allauth_signup, login

from artminster.core.apps.profile.forms import SigninForm, SignupForm

def home_url():
    try: u = reverse('home')
    except: u = "/"
    return u

def logout_view(request):
    logout(request)
    return http.HttpResponseRedirect(home_url())

def signin(request, *args, **kwargs):
    kwargs.update({
    'form_class': SigninForm,
    })

    if request.user.is_authenticated():
        return http.HttpResponseRedirect(home_url())

    # override only in case if no 'next' url provided
    if not 'next' in request.POST:
        kwargs['success_url'] = home_url()

    return login(request, *args, **kwargs)


def signup(request, *args, **kwargs):
    kwargs.update({
    'form_class': SignupForm,
    'success_url': reverse('register_complete'),
    })
    return allauth_signup(request, *args, **kwargs)