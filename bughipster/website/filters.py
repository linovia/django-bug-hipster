"""
bughipster.website.FilterSet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Filter bug list.
"""
from __future__ import print_function, division
from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _
import django_filters as filters

from bughipster.project import models


class Bug(filters.FilterSet):
    product = filters.ModelMultipleChoiceFilter(
        queryset=models.Product.objects.all(),
        to_field_name='name')
    component = filters.ModelMultipleChoiceFilter(
        queryset=models.Component.objects.all(),
        to_field_name='name')
    version = filters.ModelMultipleChoiceFilter(
        queryset=models.Version.objects.all(),
        to_field_name='value'
    )
    target_milestone = filters.ModelMultipleChoiceFilter(
        queryset=models.Milestone.objects.all(),
        to_field_name='value'
    )

    status = filters.ModelMultipleChoiceFilter(
        queryset=models.Status.objects.all(),
        to_field_name='value')
    resolution = filters.ModelMultipleChoiceFilter(
        queryset=models.Resolution.objects.all(),
        to_field_name='value')
    severity = filters.ModelMultipleChoiceFilter(
        queryset=models.Severity.objects.all(),
        to_field_name='value')
    priority = filters.ModelMultipleChoiceFilter(
        queryset=models.Priority.objects.all(),
        to_field_name='value')

    class Meta:
        model = models.Bug
        fields = [
            'product', 'component', 'version', 'target_milestone',
            'status', 'resolution', 'severity', 'priority'
        ]


class SimpleQuery(filters.FilterSet):
    bug_status = filters.ChoiceFilter(label=_('Status'), choices=(
        ('__open__', _('Open')),
        ('__closed__', _('Closed')),
        ('__all__', _('All')),
    ))
    product = filters.ModelChoiceFilter(label=_('Product'),
        queryset=models.Product.objects.all(),
        to_field_name='name', empty_label=_('All'))
    content = filters.CharFilter(label=_('Words'))
    class Meta:
        model = models.Bug
        fields = [
            'product',
        ]
