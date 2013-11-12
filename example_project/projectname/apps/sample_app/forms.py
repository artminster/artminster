from django import forms

from artminster.core.utils.form_utils import get_fieldsets_attr
from models import ModelName

class ModelNameForm(forms.ModelForm):
	
	SETS = [
		{'title': '',
			'fields': ('field_1',)},
		{'title': 'Advanced',
			'fields': ('field_3',)},
	]
	fieldsets = get_fieldsets_attr(sets=SETS)
	
	class Meta:
		model = ModelName