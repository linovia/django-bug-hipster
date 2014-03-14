"""
bughipster.project.factories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Factories for the projet's models
"""

import factory
from factory.django import DjangoModelFactory
from factory import fuzzy

from bughipster.user.factories import Profile


class Product(DjangoModelFactory):
    FACTORY_FOR = 'project.Product'

    name = factory.Sequence(lambda n: 'product{0}'.format(n))
    description = fuzzy.FuzzyText(length=32)


class Component(DjangoModelFactory):
    FACTORY_FOR = 'project.Component'

    name = factory.Sequence(lambda n: 'component{0}'.format(n))
    description = fuzzy.FuzzyText(length=32)


class Bug(DjangoModelFactory):
    FACTORY_FOR = 'project.Bug'

    title = factory.Sequence(lambda n: 'bug #{0}'.format(n))
    product = factory.SubFactory(Product)
    assignee = factory.SubFactory(Profile)
    reporter = factory.SubFactory(Profile)
