"""
bughipster.project.filters_utils
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
import django_filters as filters

from . import models


class BzChoiceFieldMixin(object):
    """
    Mixin for ModelChoiceField that allows [''] as empty value
    """
    def validate(self, value):
        # Empty value from the FilterSet
        if value == ['']:
            value = []
        super(BzChoiceFieldMixin, self).validate(value)

    def clean(self, value):
        if value == ['']:
            value = []
        return super(BzChoiceFieldMixin, self).clean(value)


class BzModelMultipleChoiceField(
        BzChoiceFieldMixin,
        forms.models.ModelMultipleChoiceField):
    """
    ModelMultipleChoiceField that allows [''] as empty value
    """
    pass


class BzModelMultipleChoiceFilter(filters.ModelMultipleChoiceFilter):
    """
    ModelMultipleChoiceFilter that allows [''] as empty value
    """
    field_class = BzModelMultipleChoiceField


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


class StatusChoiceField(BzChoiceFieldMixin, forms.MultipleChoiceField):
    def _get_choices(self):
        if self._choices:
            return self._choices
        return StatusIterator(self)

    def _set_choices(self, value):
        self._choices = self.widget.choices = list(value)

    choices = property(_get_choices, _set_choices)


class StatusFilter(filters.MultipleChoiceFilter):
    field_class = StatusChoiceField

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
        if value == [u'']:
            return qs
        q = Q()
        for v in value:
            q |= Q(**{self.name: v})
        return qs.filter(q).distinct()
