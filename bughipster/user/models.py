from __future__ import print_function, division
from __future__ import absolute_import, unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import hashers

# Make sure to import the .hashers
from . import hashers as local_hashers


@python_2_unicode_compatible
class Group(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    is_bug_group = models.SmallIntegerField(db_column='isbuggroup')
    userregexp = models.CharField(max_length=255, default='')
    active = models.SmallIntegerField(db_column='isactive', default=1)
    icon_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'groups'

    def __str__(self):
        return self.name


class ProfileManager(BaseUserManager):
    pass


@python_2_unicode_compatible
class Profile(models.Model):
    id = models.AutoField(primary_key=True, db_column='userid')
    login_name = models.CharField(max_length=255, db_index=True, unique=True)
    password = models.CharField(max_length=128, null=True, db_column='cryptpassword')
    realname = models.CharField(max_length=255, default='')
    disabledtext = models.TextField(default='')
    disable_mail = models.SmallIntegerField(default=0, blank=True)
    mybugslink = models.SmallIntegerField(default=1, blank=True)
    extern_id = models.CharField(max_length=64, null=True, blank=True,
        db_index=True, unique=True)
    is_enabled = models.SmallIntegerField(default=1, blank=True)
    last_seen_date = models.DateTimeField(null=True, blank=True) # timestamp without timezone

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'login_name'

    objects = ProfileManager()

    def __str__(self):
        return self.get_username()

    class Meta:
        db_table = 'profiles'

    def is_active(self):
        return bool(self.disabledtext)

    def get_username(self):
        return self.login_name

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = hashers.make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])
        return hashers.check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = '*'

    def has_usable_password(self):
        return hashers.is_password_usable(self.password)

    def get_full_name(self):
        return self.realname

    def get_short_name(self):
        return self.extern_id

    #
    # HACKS
    # TODO: implement those 3 functions.
    # For now this is enough to test the legacy authentication
    #
    def is_staff(self):
        return True

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm):
        return True


from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import update_last_login

user_logged_in.disconnect(update_last_login)
