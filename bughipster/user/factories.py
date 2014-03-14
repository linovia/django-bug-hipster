"""
bughipster.user.factories
~~~~~~~~~~~~~~~~~~~~~~~~~

Factories for the projet's models
"""

from factory.django import DjangoModelFactory
from factory import fuzzy
import factory


class Profile(DjangoModelFactory):
    FACTORY_FOR = 'user.Profile'

    login_name = factory.Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password',
                                                'default')
    realname = factory.Sequence(lambda n: 'Mr X{0}'.format(n))
    extern_id = fuzzy.FuzzyText(length=8)