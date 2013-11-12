BILLING_INSTALLED_APPS = (
	'artminster.contrib.billing',
	'paypal.standard.ipn',
)

# Standard IPN details
PAYPAL_SANDBOX_MODE = True
PAYPAL_RECEIVER_EMAIL = "sandbo_1318841681_biz@artminster.com"
# When in sandbox mode, you will need to login with the following to complete a test transaction:
# sandbo_1318841728_per@artminster.com / artminster18
# But to do that, you first need to go to http://developer.artminster.com with sandbox@artminster.com / artminster18