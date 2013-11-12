from django.contrib import admin

from models import Subscription, UserSubscription

class SubscriptionAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',),}
admin.site.register(Subscription, SubscriptionAdmin)

class UserSubscriptionAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'subscription', 'is_active',)
admin.site.register(UserSubscription, UserSubscriptionAdmin)