ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_SIGNUP_FORM_CLASS = None # Override this if you need to specify a custom signup form
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_PASSWORD_MIN_LENGTH = 6
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True # Attempt to bypass the signup form by using fields (e.g. username, email) retrieved from the social account provider.