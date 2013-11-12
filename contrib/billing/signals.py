from django.db.models import get_model
from django.dispatch import Signal

#-------------------------
# SENDERS
#-------------------------

# Sent when a successful user subscription is created.
new_user_subscription_created = Signal()


#-------------------------
# RECEIVERS
#-------------------------
def get_usersub_from_ipn(ipn_obj):
	"""
	Attempts to retrieve a valid SubscriptionUser record from the IPN object 
	"""
	UserSubscription = get_model('billing', 'usersubscription')
	
	usersub_id = ipn_obj.custom if len(ipn_obj.custom) > 0 else None
	usersub = None

	if usersub_id:
		try:
			usersub = UserSubscription.objects.get(id=usersub_id)
		except UserSubscription.DoesNotExist:
			#TODO: Email admin, something was wrong!
			pass
	return usersub

def signal_subscription_created(sender, **kwargs):
	"""
	Handles a successful creation of a new subscription signup
	"""
	try:
		ipn_obj = sender
		usersub = get_usersub_from_ipn(ipn_obj)
		if usersub:
			usersub.is_active = True
			usersub.save()
			new_user_subscription_created.send(sender=usersub)
	except:
		pass
		#TODO: Email admin, something was wrong!
		
def signal_subscription_cancel(sender, **kwargs):
	"""
	Handles the cancelling of a subscription signup
	"""
	try:
		ipn_obj = sender
		usersub = get_usersub_from_ipn(ipn_obj)
		if usersub:
			usersub.is_active = False
			usersub.save()
	except:
		pass
		#TODO: Email admin, something was wrong!
		
def signal_subscription_expires(sender, **kwargs):
	"""
	Handles the expiration of a subscription signup
	"""
	try:
		ipn_obj = sender
		usersub = get_usersub_from_ipn(ipn_obj)
		if usersub:
			usersub.is_active = False
			usersub.save()
	except:
		pass
		#TODO: Email admin, something was wrong!

def signal_payment_was_successful(sender, **kwargs):
	ipn_obj = sender
	#todo: Do something in here