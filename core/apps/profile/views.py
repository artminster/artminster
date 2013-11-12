from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings
from django.views.generic.base import View
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import Http404

from artminster.core.utils.view_utils import MessageMixin, LoginRequiredMixin
from artminster.core.apps.profile.forms import UserProfileForm
from utils import get_auth_profile_class

class UserProfileDetail(LoginRequiredMixin, DetailView):
	model = get_auth_profile_class()
	slug_field = 'user__username'
	slug_url_kwarg = 'username'
	template_name = "profile/userprofile_detail.html"

	def get_context_data(self, **kwargs):
		context = super(UserProfileDetail, self).get_context_data(**kwargs)
		context['profile_user'] = self.object.user
		return context

class UserProfileUpdate(MessageMixin, UpdateView):
	model = get_auth_profile_class()
	form_class = UserProfileForm
	template_name = "profile/userprofile_form.html"
	
	def get_success_url(self):
		try:
			self.success_url = reverse('profile')
		except:
			self.success_url = reverse('dashboard')
						
		return self.success_url
	
	def get_form_class(self):
		self.form_class = self.kwargs.get('form_class', self.form_class)
		return self.form_class
	
	def get_object(self, queryset=None):
		return self.request.user.profile