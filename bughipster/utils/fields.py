from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class MultiFieldPK(object):
    description = _("Composite Primary Keys")

    def __init__(self, keys=None):
        self.keys = keys
        self.primary_key = True

    def contribute_to_class(self, cls, name):
        self.name = name
        self.model = cls
        cls._meta.add_virtual_field(self)
        cls._meta.pk = self

        setattr(cls, name, self)

    def __str__(self):
        model = self.model
        app = model._meta.app_label
        return '%s.%s.%s' % (app, model._meta.object_name, self.name)
