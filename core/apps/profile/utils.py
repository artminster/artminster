from django.conf import settings
from django.db import models

def get_auth_profile_class():
	app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
	model = models.get_model(app_label, model_name)
	return model