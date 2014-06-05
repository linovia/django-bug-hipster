"""
bughipster.project.filters
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2013-2014 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import print_function, division
from __future__ import absolute_import, unicode_literals

from itertools import chain

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import django_filters as filters

from . import models
from .filters_utils import StatusFilter, BzModelMultipleChoiceFilter


#
# Bugzilla's multiple choice fields
#

class BugzillaSelectMultiple(forms.SelectMultiple):
    def render_option(self, selected_choices, option_value, option_label, pos):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        id_html = ' id=v%s_product' % (pos)
        return format_html('<option value="{0}"{1}{2}>{3}</option>',
                           option_value,
                           id_html,
                           selected_html,
                           force_text(option_label))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for pos, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            output.append(self.render_option(selected_choices, option_value, option_label, pos+1))
        return '\n'.join(output)


class SimpleQuery(filters.FilterSet):
    bug_status = filters.ChoiceFilter(label=_('Status'), choices=(
        ('__open__', _('Open')),
        ('__closed__', _('Closed')),
        ('__all__', _('All')),
    ), name='status')
    product = filters.ModelChoiceFilter(label=_('Product'),
        queryset=models.Product.objects.all(),
        to_field_name='name', empty_label=_('All'))
    content = filters.CharFilter(label=_('Words'))

    class Meta:
        model = models.Bug
        fields = [
            'bug_status', 'product',
        ]


class ComplexQuery(filters.FilterSet):
    product = BzModelMultipleChoiceFilter(
        queryset=models.Product.objects.all(),
        to_field_name='name', widget=BugzillaSelectMultiple, required=False)
    component = BzModelMultipleChoiceFilter(
        queryset=models.Component.objects.all(),
        to_field_name='name')
    bug_status = BzModelMultipleChoiceFilter(
        queryset=models.Status.objects.all(),
        to_field_name='value')
    resolution = BzModelMultipleChoiceFilter(
        queryset=models.Resolution.objects.all(),
        to_field_name='value')

    class Meta:
        model = models.Bug
        fields = [
            'product', 'component', 'bug_status', 'resolution'
        ]

class FullQuery(ComplexQuery):
    bug_status = StatusFilter(name='status')
