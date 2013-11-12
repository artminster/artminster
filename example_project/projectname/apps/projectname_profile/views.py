from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings
from django.views.generic.base import View
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import Http404

from artminster.core.utils.view_utils import MessageMixin, LoginRequiredMixin
from artminster.core.apps.profile.utils import get_auth_profile_class

from forms import UserProfileForm

class UserProfileUpdate(LoginRequiredMixin, MessageMixin, UpdateView):
	model = get_auth_profile_class()
	form_class = UserProfileForm
	template_name = "profile/userprofile_form.html"

	def get_object(self, queryset=None):
		return self.request.user.profile