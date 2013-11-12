from django import http
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

from artminster.core.apps.profile.models import UserProfile
from artminster.core.apps.profile.forms import ProfileForm

from artminster.core.utils.view_utils import main_render

@main_render(template='profile/public.html')
def profile(request, username):
    """
    detailed profile
    """
    
    user = get_object_or_404(User, username = username)
    profile = user.profile

    return {'profile':profile}

@login_required
@main_render(template='profile/edit_profile.html')
def edit_profile(request):
    """
    edit profile
    """

    user = request.user
    
    profile = user.profile
    initial = {'first_name': user.first_name, 'last_name': user.last_name}
    
    form = ProfileForm(request.POST or None, request.FILES or None, instance = profile, initial = initial)
    if request.method == 'POST' and form.is_valid():
        profile = form.save()
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()   

        return http.HttpResponseRedirect(reverse('dashboard', args=()))

    return {'form':form, 'profile':profile}


@main_render(template='account/signup_complete.html')
def register_complete(request):
    if request.user.is_authenticated():
        logout(request)
        return http.HttpResponseRedirect(reverse('register_complete', args=()))
    else:
        return {}