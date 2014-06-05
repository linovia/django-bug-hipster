"""
bughipster.project.forms
~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django import forms
from django.utils import six
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field
from related_choice_field.fields import RelatedModelMultipleChoiceField
from . import models


#
# Bug form for creating new bugs
#
class Bug(forms.ModelForm):
    version = forms.ModelChoiceField(queryset=models.Version.objects, empty_label=None)
    component = forms.ModelChoiceField(queryset=models.Component.objects, empty_label=None)

    class Meta:
        model = models.Bug
        fields = (
            'component', 'version', 'severity', 'os', 'priority',
            'status', 'assignee', 'cc', 'deadline', 'alias',
            # 'url', 'summary', 'estimate', 
            # 'blocks', 'description', 'dependson','hardware', 
        )

    def __init__(self, product_id, *args, **kwargs):
        self.product_id = product_id
        super(Bug, self).__init__(*args, **kwargs)

        # Limit the available components to the project's
        qs = self.fields['component'].queryset
        self.fields['component'].queryset = qs.filter(product_id=self.product_id)

        # Limit the available versions to the project's
        qs = self.fields['version'].queryset
        self.fields['version'].queryset = qs.filter(product_id=self.product_id)
        self.configure_helper()

    def configure_helper(self):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('component', size=7, aria_required='true', onchange='set_assign_to();', css_class='required'),
            Fieldset(
                'tada',
                'version',
                'severity',
                'os',
                'priority',
                'status',
                'assignee',
                'cc',
                'deadline',
                'alias',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )


#
# Complex Bug Search
#
from django.utils.encoding import force_text
from itertools import chain
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class BugzillaSelectMultiple(forms.SelectMultiple):
    def render_option(self, selected_choices, option_value, option_label, option_id):
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
        id_html = mark_safe(' id="v%s_product"' % str(option_id))
        return format_html('<option value="{0}"{1}{2}>{3}</option>',
                           option_value,
                           selected_html,
                           id_html,
                           force_text(option_label))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_id, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{0}">', force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label, option_id))
        return '\n'.join(output)


class BugzillaModelChoiceIterator(object):
    def __init__(self, field):
        self.field = field
        self.queryset = field.queryset

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    self.choice(obj) for obj in self.queryset.all()
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
            for obj in self.queryset.all():
                yield self.choice(obj)

    def __len__(self):
        return (len(self.queryset) +
            (1 if self.field.empty_label is not None else 0))

    def choice(self, obj):
        return (self.field.prepare_value(obj), obj.id, self.field.label_from_instance(obj))


class BugzillaMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    Custom ModelMultipleChoiceField to:
    1) use the right widget
    2) Use a custom iterator that use the object's value instead of the id
    """
    widget = BugzillaSelectMultiple

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return BugzillaModelChoiceIterator(self)

    choices = property(_get_choices, forms.ChoiceField._set_choices)


class ComplexBugSearch(forms.Form):
    # product = filters.ModelMultipleChoiceFilter(
    #     queryset=models.Product.objects.all(),
    #     to_field_name='name', widget=BugzillaSelectMultiple)
    product = BugzillaMultipleChoiceField(
        queryset=models.Product.objects.all(),
        to_field_name='name')
    # component = filters.ModelMultipleChoiceFilter(
    #     queryset=models.Component.objects.all(),
    #     to_field_name='name')
    component = BugzillaMultipleChoiceField(
        queryset=models.Component.objects.all())
    # bug_status = filters.ModelMultipleChoiceFilter(
    #     queryset=models.Status.objects.all(),
    #     to_field_name='value')
    # resolution = filters.ModelMultipleChoiceFilter(
    #     queryset=models.Resolution.objects.all(),
    #     to_field_name='value')

    # class Meta:
    #     model = models.Bug
    #     fields = [
    #         'product', 'component', 'bug_status', 'resolution'
    #     ]
