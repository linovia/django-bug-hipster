from __future__ import unicode_literals

import hashlib
import base64
import re

from django.contrib.auth import hashers
from django.utils.encoding import force_bytes
from django.utils.crypto import constant_time_compare, get_random_string
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_noop as _
from django.contrib.auth import forms as admin_forms


SALT_SIZE = 8
HASH_REGEXP = '(?P<salt>\S{%i})(?P<encoded_password>\S+){(?P<algo>\S+)}'
HASH_COMPILED_REGEXP = re.compile(HASH_REGEXP % SALT_SIZE)

#
# HUGE HACK
# Monkey patch UNUSABLE_PASSWORD
#
hashers.UNUSABLE_PASSWORD = '*'


def identify_hasher(encoded):
    """
    Returns an instance of a loaded password hasher.

    Identifies hasher algorithm by examining encoded hash, and calls
    get_hasher() to return hasher. Raises ValueError if
    algorithm cannot be identified, or if hasher is not loaded.
    """
    if not hashers.HASHERS:
        hashers.load_hashers()

    for hasher in hashers.HASHERS.values():
        if hasattr(hasher, 'can_handle') and \
                hasher.can_handle(encoded):
            return hasher

    raise ValueError("No hasher matching the encoded data found. "
                     "Did you specify it in the PASSWORD_HASHERS setting ?")

hashers.identify_hasher = identify_hasher
admin_forms.identify_hasher = identify_hasher


class BugzillaHasher(hashers.BasePasswordHasher):
    """
    The SHA1 password hashing algorithm (not recommended)
    """
    algorithm = "SHA-256"

    def can_handle(self, encoded):
        """
        Checks if this hasher can handle a given encoded password scheme
        """
        result = HASH_COMPILED_REGEXP.search(encoded)
        if not result:
            return False
        try:
            salt, hashed, algorithm = result.groups()
        except:
            return False
        return algorithm == self.algorithm

    @hashers.password_max_length(hashers.MAXIMUM_PASSWORD_LENGTH)
    def encode(self, password, salt):
        assert password
        assert salt and len(salt) == SALT_SIZE
        hashed = base64.b64encode(
            hashlib.sha256(
                force_bytes(password + salt)).digest())
        if hashed[-1] == '=':
            hashed = hashed[:-1]
        return '%s%s{%s}' % (salt, hashed, self.algorithm)

    @hashers.password_max_length(hashers.MAXIMUM_PASSWORD_LENGTH)
    def verify(self, password, encoded):
        salt, hashed, algorithm = HASH_COMPILED_REGEXP.search(encoded).groups()
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt)
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        salt, hashed, algorithm = HASH_COMPILED_REGEXP.search(encoded).groups()
        assert algorithm == self.algorithm
        return SortedDict([
            (_('algorithm'), algorithm),
            (_('salt'), hashers.mask_hash(salt, show=2)),
            (_('hash'), hashers.mask_hash(hashed)),
        ])

    def salt(self):
        """
        Generates a cryptographically secure nonce salt in ascii
        """
        return get_random_string(8)
