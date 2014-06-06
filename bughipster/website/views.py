"""
bughipster.website.views
~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django import http
from django.views import generic
from django.core.urlresolvers import reverse

from bughipster.project import models, filters


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


class SimpleQuery(generic.TemplateView):
    template_name = 'simple_search.html'

    def get_context_data(self, **kwargs):
        result = super(SimpleQuery, self).get_context_data(**kwargs)
        # f = ProductFilter(request.GET, queryset=Product.objects.all())
        result['form'] = filters.SimpleQuery({}, queryset=models.Bug.objects.all()).form
        return result


#
# Complex query page helpers
#
def item_per_project(items):
    """
    Create a dictionary of {project_id: [item_ids]} which allows the page
    to show/hide items according to the project id.

    - items is a list of item
    - item must have an id
    - item must have an associated project
    """
    result = {}
    for item in items:
        result.setdefault(item.product_id, []).append(item.id)
    return result


def remove_duplicates(items):
    """
    Remove duplicated names from the available choices.
    Returns the cleaned list and the duplicates dictionary
    """
    items_map = {}
    duplicates = {}
    duplicates_count = {}

    for item in items:
        items_map.setdefault(item.value, []).append(item.id)

    for grouped_items in items_map.values():
        if len(grouped_items) > 1:
            reference = grouped_items.pop()
            local_dict = dict((item, reference) for item in grouped_items)
            duplicates.update(local_dict)
            duplicates_count[reference] = len(local_dict)
    return duplicates, duplicates_count


class ComplexQuery(generic.TemplateView):
    template_name = 'complex_search.html'

    def get_context_data(self, **kwargs):
        result = super(ComplexQuery, self).get_context_data(**kwargs)

        # Generic data
        result['statuses'] = list(models.Status.objects.all().order_by('sortkey', 'value'))
        result['resolutions'] = list(models.Resolution.objects.all().order_by('sortkey', 'value').distinct())

        # TODO: Check project's permission.
        result['projects'] = list(models.Product.objects.all().order_by('name'))
        result['components'] = list(models.Component.objects.all().order_by('product__id', 'name').distinct())
        result['versions'] = list(models.Version.objects.all().order_by('id').distinct())

        # Sort the components/version/other per project
        result['per_project'] = dict((key, item_per_project(result[key])) for key in ['components', 'versions'])

        # Filter the various values based on authorized projects.
        return result


def query(request, *args, **kwargs):
    view_type = request.GET.get('format', 'specific')
    if view_type == 'specific':
        return SimpleQuery.as_view()(request, *args, **kwargs)
    elif view_type == 'advanced':
        return ComplexQuery.as_view()(request, *args, **kwargs)

    error_message =  """The requested format <em>%s</em> does not exist with
    a content type of <em>html</em>.""" % (view_type,)

    return Error.as_view(message=error_message)(request, *args, **kwargs)
