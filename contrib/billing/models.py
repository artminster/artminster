from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse

from artminster.core.utils.fields import AutoOneToOneField
from artminster.core.utils.comms import create_threaded_email
from artminster.core.utils.abstract_models import BaseModel, TitleAndSlugModel
from artminster.core.utils.datetime_utils import add_months, monthdelta
from artminster.contrib.billing.settings import CURRENCIES, SUBSCRIPTION_FREQUENCIES
from signals import signal_subscription_created, signal_payment_was_successful, signal_subscription_cancel, signal_subscription_expires

from paypal.standard.ipn.signals import payment_was_successful, subscription_signup, recurring_create, subscription_cancel, subscription_eot

from datetime import datetime, date
import time

class Subscription(TitleAndSlugModel):
	"""
	A subscription definition
	"""
	description = models.TextField(null=True, blank=True)
	currency = models.CharField(max_length=10, choices=CURRENCIES)
	frequency = models.CharField(max_length=10, choices=SUBSCRIPTION_FREQUENCIES, default="MONTHLY")
	frequency_duration = models.IntegerField(default=1, help_text="Duration of each frequency (i.e. every X days / weeks / months etc) ")
	price = models.DecimalField(decimal_places=2, max_digits=10)
	is_active = models.BooleanField(default=False)

	def __unicode__(self):
		return "%s (%s %s)" % (self.title, self.price, self.currency)
		
class UserSubscription(BaseModel):
	"""
	A record indicating which subscription a user has signed up to
	"""
	subscription = models.ForeignKey(Subscription)
	user = models.ForeignKey(User)
	is_active = models.BooleanField(default=False)

	@property
	def date_of_this_cycle_start(self):
		# Returns the date of this cycle
		invalid_date = True
		day_start = self.created.day
		while invalid_date:
			try:
				cycle_start = date(datetime.now().year, datetime.now().month, day_start)
				invalid_date = False
			except:
				day_start = day_start - 1
		return cycle_start
	
	@property
	def date_of_next_cycle_reset(self):
		# Returns the date of the next subscription cycle
		# TODO: Only setup for monthly based, need to cater for other cycles
		invalid_date = True
		day_start = self.created.day
		while invalid_date:
			try:
				if datetime.now().month == 12:
					next_cycle_reset = date(datetime.now().year+1, 1, day_start)
				else:
					next_cycle_reset = date(datetime.now().year, datetime.now().month+1, day_start)
				invalid_date = False
			except:
				day_start = day_start - 1
		return next_cycle_reset
	
	def save(self, *args, **kwargs):
		super(UserSubscription, self).save(*args, **kwargs)
		
		# Delete all other entries for this user, so we only have one active one
		if self.is_active:
			all_other_subs = UserSubscription.objects.filter(user=self.user).exclude(subscription=self.subscription)
			all_other_subs.delete()
	
	def __unicode__(self):
		return "%s (%s)" % (self.user, self.subscription)
		

# SIGNALS
subscription_signup.connect(signal_subscription_created)
subscription_cancel.connect(signal_subscription_cancel)
subscription_eot.connect(signal_subscription_expires)
payment_was_successful.connect(signal_payment_was_successful)