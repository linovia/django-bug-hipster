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
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import django_filters as filters

from bughipster.project import models


#
# Status filter: all the status states plus __open__ & __closed__ & __all__
#

class StatusIterator(object):

    def __init__(self, field):
        self.field = field
        self.queryset = models.Status.objects.all()

    def __iter__(self):
        yield ('__all__',    _('All'))
        yield ('__open__',   _('Open'))
        yield ('__closed__', _('Closed'))
        for obj in self.queryset.all():
            yield self.choice(obj)

    def __len__(self):
        return (3 + len(self.queryset))

    def choice(self, obj):
        return (obj.value, obj.value)


class StatusModelChoiceField(forms.MultipleChoiceField):
    def _get_choices(self):
        if self._choices:
            return self._choices
        return StatusIterator(self)

    def _set_choices(self, value):
        self._choices = self.widget.choices = list(value)

    choices = property(_get_choices, _set_choices)


class StatusFilter(filters.MultipleChoiceFilter):
    field_class = StatusModelChoiceField

    def filter(self, qs, value):
        value = value or ()

        if value == ['__open__']:
            return qs.opened().distinct()
        if value == ['__closed__']:
            return qs.closed().distinct()
        if value == ['__all__']:
            return qs.all().distinct()

        if len(value) == len(self.field.choices):
            return qs
        q = Q()
        for v in value:
            q |= Q(**{self.name: v})
        return qs.filter(q).distinct()


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
    product = filters.ModelMultipleChoiceFilter(
        queryset=models.Product.objects.all(),
        to_field_name='name', widget=BugzillaSelectMultiple)
    component = filters.ModelMultipleChoiceFilter(
        queryset=models.Component.objects.all(),
        to_field_name='name')
    bug_status = filters.ModelMultipleChoiceFilter(
        queryset=models.Status.objects.all(),
        to_field_name='value')
    resolution = filters.ModelMultipleChoiceFilter(
        queryset=models.Resolution.objects.all(),
        to_field_name='value')

    class Meta:
        model = models.Bug
        fields = [
            'product', 'component', 'bug_status', 'resolution'
        ]

class FullQuery(ComplexQuery):
    bug_status = StatusFilter(name='status')
