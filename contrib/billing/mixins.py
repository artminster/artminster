from models import UserSubscription

class UserWithSubscriptionMixin():
	"""
	A mixin to be added to the UserProfile model, for when a project makes use of user subscriptions
	"""
	
	@property
	def has_active_subscription(self):
		# Simply returns True if this user has an active subscription
		if self.user_subscription: return True
		else: return False
		
	@property
	def user_subscription(self):
		# Returns the Subscription linked to this user (if there is one)
		try:
			usersub = UserSubscription.objects.get(user=self.user, is_active=True).subscription
		except UserSubscription.DoesNotExist:
			usersub = None
		return usersub
	
	class Meta:
		abstract = True