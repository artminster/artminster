from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from artminster.core.apps.profile.utils import get_auth_profile_class

class UserProfileInline(admin.StackedInline):
	model = get_auth_profile_class()

class MyUserAdmin(UserAdmin):
	list_display = ('username','email','first_name','last_name','date_joined','last_login','is_staff', 'is_active')
	list_editable = ['is_active']
	inlines = [ UserProfileInline ]

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)