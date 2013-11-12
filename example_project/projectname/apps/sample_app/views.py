from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from artminster.core.utils.view_utils import MessageMixin, LoginRequiredMixin
from models import ModelName
from forms import ModelNameForm

"""
Base ModelName views 
"""
class Index(LoginRequiredMixin, TemplateView):
	template_name = "appname/modelnames_index.html"

	def get_context_data(self, **kwargs):
		items = ModelName.objects.all()
		return {'items': items}
		
class ModelNameDetail(LoginRequiredMixin, DetailView):
	model = ModelName

	def get_context_data(self, **kwargs):
		context = super(ModelNameDetail, self).get_context_data(**kwargs)
		return context
		
class ModelNameCreate(LoginRequiredMixin, MessageMixin, CreateView):
	model = ModelName
	form_class = ModelNameForm

class ModelNameUpdate(LoginRequiredMixin, MessageMixin, UpdateView):
	model = ModelName
	form_class = ModelNameForm

class ModelNameDelete(LoginRequiredMixin, MessageMixin, DeleteView):
	model = ModelName
	success_url = reverse_lazy('modelname_index')