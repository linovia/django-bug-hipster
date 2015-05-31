"""
bughipster.project.factories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2013-2014 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import factory
from factory.django import DjangoModelFactory
from factory import fuzzy

from bughipster.user.factories import Profile
from . import models


class Product(DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.Sequence(lambda n: 'product{0}'.format(n))
    description = fuzzy.FuzzyText(length=32)


class Component(DjangoModelFactory):
    class Meta:
        model = models.Component

    name = factory.Sequence(lambda n: 'component{0}'.format(n))
    description = fuzzy.FuzzyText(length=32)


class Bug(DjangoModelFactory):
    class Meta:
        model = models.Bug

    title = factory.Sequence(lambda n: 'bug #{0}'.format(n))
    product = factory.SubFactory(Product)
    assignee = factory.SubFactory(Profile)
    reporter = factory.SubFactory(Profile)
