"""
bughipster.project.views
~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Xavier Ordoquy,
see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django.views import generic

from . import models


def bug_creation(request, *args, **kwargs):
    if not request.GET.get('product', None):
        return SelectProduct.as_view()(request, *args, **kwargs)
    return CreateBug.as_view()(request, *args, **kwargs)


class CreateBug(generic.CreateView):
    template_name = 'new_bug.html'
    model = models.Bug


class SelectProduct(generic.ListView):
    template_name = 'product_selection.html'
    model = models.Product
