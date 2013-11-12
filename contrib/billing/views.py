from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings

from artminster.core.utils.view_utils import MessageMixin, LoginRequiredMixin
from paypal.standard.forms import PayPalPaymentsForm

from models import Subscription, UserSubscription

"""
Base billing views 
"""
class MyAccount(LoginRequiredMixin, TemplateView):
	template_name = "billing/my_account.html"

	def get_context_data(self, **kwargs):
		try:
			usersub = UserSubscription.objects.get(user=self.request.user, is_active=True)
		except UserSubscription.DoesNotExist:
			usersub = None
		
		context = super(MyAccount, self).get_context_data(**kwargs)
		context['usersub'] = usersub
		return context

"""
Subscription views 
"""
class SubscriptionSignup(LoginRequiredMixin, DetailView):
	model = Subscription
	template_name = "billing/subscription_signup.html"

	def get_context_data(self, **kwargs):
		usersub, created = UserSubscription.objects.get_or_create(user=self.request.user, subscription=self.object)
		if created:
			usersub.is_active = False
			usersub.save()
		
		# Setup the paypal dict required for this subscription
		paypal_dict = {
			"cmd": "_xclick-subscriptions",
			"business": settings.PAYPAL_RECEIVER_EMAIL,
			"a3": "%s" % self.object.price,					# price 
			"p3": self.object.frequency_duration,				# duration of each unit (depends on unit)
			"t3": self.object.frequency,						# duration unit ("M for Month")
			"src": "1",										# make payments recur
			"sra": "1",										# reattempt payment on payment error
			"no_note": "1",									# remove extra notes (optional)
			"custom": "%s" % usersub.id,						# the ID of the usersub  (for us to reference later)
			"item_name": self.object.title,
			"notify_url": "%s%s" % (settings.PROJECT_DOMAIN, reverse('paypal-ipn')),
			"return_url": "%s%s" % (settings.PROJECT_DOMAIN, reverse('subscription_complete', args=[self.object.slug])),
			"cancel_return": "%s%s" % (settings.PROJECT_DOMAIN, reverse('subscription_cancel', args=[self.object.slug])),
		}
		form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
		
		context = super(SubscriptionSignup, self).get_context_data(**kwargs)
		context['form'] = form
		context['usersub'] = usersub
		return context
		
class SubscriptionComplete(LoginRequiredMixin, DetailView):
	model = Subscription
	template_name = "billing/subscription_complete.html"

	def get_context_data(self, **kwargs):
		context = super(SubscriptionComplete, self).get_context_data(**kwargs)
		return context
		
class SubscriptionCancel(LoginRequiredMixin, DetailView):
	model = Subscription
	template_name = "billing/subscription_cancel.html"

	def get_context_data(self, **kwargs):
		context = super(SubscriptionCancel, self).get_context_data(**kwargs)
		return context