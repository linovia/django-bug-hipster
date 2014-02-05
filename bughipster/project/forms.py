"""
bughipster.project.forms
~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Xavier Ordoquy,
see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django import forms
from . import models


class Bug(forms.ModelForm):
    class Meta:
        model = models.Bug
        fields = (
            'component', 'version', 'severity', 'os', 'priority',
            'status', 'assignee', 'cc', 'deadline', 'alias',
            # 'url', 'summary', 'estimate', 
            # 'blocks', 'description', 'dependson','hardware', 
        )