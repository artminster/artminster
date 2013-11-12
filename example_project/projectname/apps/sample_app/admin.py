from django.contrib import admin

from models import ModelName

class ModelNameAdmin(admin.ModelAdmin):
	pass
admin.site.register(ModelName, ModelNameAdmin)