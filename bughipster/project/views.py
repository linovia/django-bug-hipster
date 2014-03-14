"""
bughipster.project.views
~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Xavier Ordoquy,
see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django_filters.views import FilterView
from django.views import generic
from django import http

from . import models
from . import forms
from . import filters


class ProjectRestrictedMixin(object):
    def dispatch(self, request, *args, **kwargs):
        product_name = request.GET.get('product', None)
        try:
            self.product = models.Product.objects.get(name=product_name)
        except models.Product.DoesNotExist:
            return http.Http404()

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(ProjectRestrictedMixin, self).get_context_data(**kwargs)
        data['product'] = self.product
        return data


class CreateBug(ProjectRestrictedMixin, generic.CreateView):
    template_name = 'new_bug.html'
    model = models.Bug
    form_class = forms.Bug

    def get_form_kwargs(self):
        kwargs = super(CreateBug, self).get_form_kwargs()
        kwargs['product_id'] = self.product.id
        return kwargs


class SelectProduct(generic.ListView):
    template_name = 'product_selection.html'
    model = models.Product


def bug_creation(request, *args, **kwargs):
    if not request.GET.get('product', None):
        return SelectProduct.as_view()(request, *args, **kwargs)
    return CreateBug.as_view()(request, *args, **kwargs)


class BugList(FilterView):
    template_name = 'bug_list.html'
    model = models.Bug
    filterset_class = filters.SimpleQuery
