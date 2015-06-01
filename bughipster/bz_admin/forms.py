"""
bughipster.bz_admin.forms
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2015 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django import forms


#
# form to create a new Product
#

# TODO: define a PROJECT_NAME_MAX_LENGTH, COMPONENT_NAME_MAX_LENGTH, INITIALOWNER_MAX_LENGTH
class EditProduct(forms.Form):
    product = forms.CharField(max_length=64)
    description = forms.CharField()
    is_active = forms.NullBooleanField()
    allows_unconfirmed = forms.NullBooleanField()

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
    initialowner = forms.CharField(max_length=255)

    def get_message_from_errors(self):
        """
        Translate Django's errors into Bugzilla's one.
        """
        result = super(NewProduct, self).get_message_from_errors()
        if not result:
            return result
        if 'comp_desc' in self.errors:
            return "You must enter a non-blank description for this component."
        elif 'initialowner' in self.errors:
            return "A default assignee is required for this component."
        elif 'component' in self.errors:
            return "You must enter a name for this new component."
