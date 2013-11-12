from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse

from filebrowser.fields import FileBrowseField
from artminster.core.utils.fields import AutoOneToOneField
from artminster.core.utils.abstract_models import BaseModel, TitleAndSlugModel

class ModelName(TitleAndSlugModel):
	"""
	Enter your description here
	"""
	
	def get_absolute_url(self):
		return reverse("modelname_detail", args=[self.slug])

	def __unicode__(self):
		return self.slug