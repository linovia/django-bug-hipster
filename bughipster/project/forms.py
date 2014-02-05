"""
bughipster.project.forms
~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Xavier Ordoquy,
see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from . import models


class Bug(forms.ModelForm):
    version = forms.ModelChoiceField(queryset=models.Version.objects, empty_label=None)
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

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
