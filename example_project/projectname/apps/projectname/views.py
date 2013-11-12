from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from artminster.core.utils.view_utils import MessageMixin

"""
Base projectname views 
"""
class Home(TemplateView):
	template_name = "projectname/home.html"

	def get_context_data(self, **kwargs):
		return {}