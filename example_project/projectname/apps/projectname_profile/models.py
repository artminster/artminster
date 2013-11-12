from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template import loader, Context
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
import re, unicodedata
import datetime

from filebrowser.fields import FileBrowseField
from artminster.core.utils.fields import AutoOneToOneField
from artminster.core.utils.abstract_models import BaseModel
from artminster.core.apps.profile.models import UserProfile as _UserProfile  

class UserProfile(_UserProfile):
	"""
	Profile and configurations for a user
	"""
	
	bio = models.TextField(null=True, blank=True)

	def __unicode__(self):
		if self.user.first_name:
			return "%s %s" % (self.user.first_name, self.user.last_name)
		else:
			return self.user.username