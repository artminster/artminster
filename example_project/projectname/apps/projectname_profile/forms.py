from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from allauth.account.forms import LoginForm

from artminster.core.utils.form_utils import get_fieldsets_attr
from artminster.core.apps.profile.forms import UserProfileForm as _UserProfileForm
from artminster.core.apps.profile.utils import get_auth_profile_class

class UserProfileForm(_UserProfileForm):
	#SETS = [
	#	{'title': '',
	#		'fields': ('first_name', 'last_name', 'address_line_1', 'city', 'state', 'zipcode', 'country', 'email', 'phone')},
	#]
	#fieldsets = get_fieldsets_attr(sets=SETS)
	pass