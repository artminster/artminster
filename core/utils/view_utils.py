from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.core.urlresolvers import get_mod_func
from django.conf import settings
from django.utils.functional import Promise
from datetime import datetime
from django.contrib import messages

from artminster.core.utils.decorators import render_to

import simplejson

"""
    View decorators and utils to assist in the view architecture we have in use here. You shouldn't need to amend anything here.
"""

class MessageMixin(object):
    """
    Make it easy to display notification messages when using Class Based Views.
    """
    def delete(self, request, *args, **kwargs):
        if not hasattr(self, 'success_message'):
            self.success_message = "The record was deleted successfully."

        messages.success(self.request, self.success_message)
        return super(MessageMixin, self).delete(request, *args, **kwargs)

    def form_valid(self, form):
        if not hasattr(self, 'success_message'):
            self.success_message = "The record was saved successfully."
        messages.success(self.request, self.success_message)
        return super(MessageMixin, self).form_valid(form)

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class JSONEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, Promise):
            return force_unicode(o)
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            return super(JSONEncoder, self).default(o)

class JSONResponse(HttpResponse):
    def __init__(self, data):
        HttpResponse.__init__(
            self, content=simplejson.dumps(data, cls=JSONEncoder),
            #mimetype="text/html",
        )

class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(
            self.convert_context_to_json(context),
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return simplejson.dumps(context)