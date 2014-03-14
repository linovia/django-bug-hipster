"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from bughipster.user.hashers import BugzillaHasher


class HasherTest(TestCase):
    def test_encode(self):
        encoded = "c56mZDsJ3qtdtvemXXw8v4P8mKTKetIDNtKneGM2q9Xek9mfWA0{SHA-256}"
        hasher = BugzillaHasher()
        result = hasher.encode('pipoti', "c56mZDsJ")
        assert result == encoded, result

    def test_verify(self):
        encoded = "c56mZDsJ3qtdtvemXXw8v4P8mKTKetIDNtKneGM2q9Xek9mfWA0{SHA-256}"
        hasher = BugzillaHasher()
        assert hasher.verify('pipoti', encoded)
        assert not hasher.verify('pipot', encoded)

    def test_safe_summary(self):
        encoded = "c56mZDsJ3qtdtvemXXw8v4P8mKTKetIDNtKneGM2q9Xek9mfWA0{SHA-256}"
        hasher = BugzillaHasher()
        assert hasher.safe_summary(encoded) == {
            'algorithm': 'SHA-256',
            'salt': 'c5******',
            'hash': '3qtdtv*************************************'
        }
