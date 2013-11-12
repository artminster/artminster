from django.conf import settings

CURRENCIES = getattr(settings, "BILLING_CURRENCIES",
	(
		('USD','USD'),
		('GBP','GBP'),
		('EUR','EUR'),
	)
)

SUBSCRIPTION_FREQUENCIES = (
	('D', 'Daily'),
	('W', 'Weekly'),
	('M', 'Monthly'),
	('Y', 'Yearly'),
	('NONE', 'N/A (Subscription is Free)'),
)