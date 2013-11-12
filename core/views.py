from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django import http
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.db.models import Q
from django.template import Context, loader, RequestContext
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token

@requires_csrf_token
def server_error(request, template_name='500.html'):
	"""
	500 error handler.

	Templates: `500.html`
	Context: None
	"""
	t = loader.get_template(template_name) # You need to create a 500.html template.
	return http.HttpResponseServerError(t.render(RequestContext(request, {'request_path': request.path, 'STATIC_URL':settings.STATIC_URL, 'MEDIA_URL':settings.MEDIA_URL})))