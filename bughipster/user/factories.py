"""
bughipster.user.factories
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2013-2014 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from factory import fuzzy
import factory


class Profile(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    login_name = factory.Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password',
                                                'default')
    realname = factory.Sequence(lambda n: 'Mr X{0}'.format(n))
    extern_id = fuzzy.FuzzyText(length=8)
