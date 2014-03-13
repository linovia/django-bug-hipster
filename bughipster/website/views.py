"""
bughipster.website.views
~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Xavier Ordoquy,
see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django import http
from django.views import generic
from django.core.urlresolvers import reverse


class ToDo(generic.TemplateView):
    template_name = 'todo.html'


class Error(generic.TemplateView):
    template_name = 'error.html'
    message = None

    def get_context_data(self, **kwargs):
        result = super(Error, self).get_context_data(**kwargs)
        result['message'] = self.message
        return result


class Home(generic.TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if 'logout' in self.request.GET:
            return http.HttpResponseRedirect(reverse('logout'))
        if self.request.GET:
            raise ValueError(self.request.GET)
        return super(Home, self).get(request, *args, **kwargs)


class UnconfiguredHome(generic.TemplateView):
    template_name = 'unconfigured.html'


class CreateAccount(generic.TemplateView):
    template_name = 'create_account.html'


class Query(generic.TemplateView):
    template_name = 'search.html'
