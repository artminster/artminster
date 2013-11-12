from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
import re, unicodedata

from filebrowser.fields import FileBrowseField
from artminster.core.utils.fields import AutoOneToOneField
from artminster.core.utils.abstract_models import BaseModel

class UserProfile(BaseModel):
    """
    Profile and configurations for a user
    """
    user = AutoOneToOneField(User, related_name="profile", editable=False)
    
    class Meta:
        abstract = True
        
    def get_absolute_url(self):
        return reverse('profile', args=[self.user.username])

    def username(self):
        return self.user.username
    
    def first_name(self):
        return self.user.first_name
    
    def last_name(self):
        return self.user.last_name
    
    def __unicode__(self):
        user = self.user
        if user.first_name:
            return "%s %s" % (user.first_name, user.last_name)
        else:
            return user.username