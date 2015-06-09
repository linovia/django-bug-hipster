"""
bughipster.bz_admin.forms
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2015 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django import forms
from bughipster.user import models as user_models


#
# form to create a new Product
#

# TODO: define a PROJECT_NAME_MAX_LENGTH
# TODO: define a COMPONENT_NAME_MAX_LENGTH
# TODO: define a INITIALOWNER_MAX_LENGTH
class EditProduct(forms.Form):
    product = forms.CharField(max_length=64)
    description = forms.CharField()
    is_active = forms.BooleanField(required=False)
    allows_unconfirmed = forms.BooleanField(required=False)

    def get_message_from_errors(self):
        """
        Translate Django's errors into Bugzilla's one.
        """
        if 'product' in self.errors:
            return "You must enter a name for the product."
        elif 'description' in self.errors:
            return "You must enter a description for this product."


class NewProduct(EditProduct):
    product = forms.CharField(max_length=64)
    description = forms.CharField()
    is_active = forms.NullBooleanField()
    allows_unconfirmed = forms.NullBooleanField()

    createseries = forms.NullBooleanField()

    version = forms.CharField(max_length=64)
    component = forms.CharField(max_length=64)
    comp_desc = forms.CharField()
    initialowner = forms.ModelChoiceField(
        queryset=user_models.Profile.objects.all(),
        to_field_name='login_name',
    )

    def get_message_from_errors(self):
        """
        Translate Django's errors into Bugzilla's one.
        """
        result = super(NewProduct, self).get_message_from_errors()
        if result:
            return result
        if 'comp_desc' in self.errors:
            return "You must enter a non-blank description for this component."
        elif 'initialowner' in self.errors:
            if self.errors['initialowner'] == [
                    'Select a valid choice. That choice is not one of the '
                    'available choices.']:
                # TODO: make sure the message matches the Bugzilla message
                return (
                    "Bugzilla was unable to make any match at all for one "
                    "or more of the names and/or email addresses you entered "
                    "on the previous page."
                )
            return "A default assignee is required for this component."
        elif 'component' in self.errors:
            return "You must enter a name for this new component."
