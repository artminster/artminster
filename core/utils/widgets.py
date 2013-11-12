from itertools import chain
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django import forms
from django.db.models import get_model
from django.utils import simplejson
from django.template.loader import render_to_string
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.conf import settings

from PIL import Image

import os
   
class FileBrowserFrontendWidget(forms.FileInput):
    def __init__(self, attrs=None):
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}
    
    def render(self, name, value, attrs=None):
        if value is None:
            value = ""
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        return render_to_string("filebrowser/custom_field_frontend.html", locals())
