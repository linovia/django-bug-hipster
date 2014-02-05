"""
bughipster.project.models
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Xavier Ordoquy,
see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from __future__ import print_function, division
from __future__ import absolute_import, unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models

from compositekey import db

# TODO:
# Manage the field type #7
# Manage the field type #3
# Rename op_sys -> os
# Rename rep_platform -> Domain


CF_TYPE_CHOICES = (
    (0, 'Unknown'),
    (1, 'Free text'),
    (2, 'Single select'),
    (3, 'Multi select'),
    (4, 'Text area'),
    (5, 'Datetime'),
    (6, 'Bug id'),
    (7, 'Bug urls'),
)


CF_TYPE_MAPPING = [
    None,
    (models.CharField, {'max_length': 255, 'null': True, 'blank': True}),
    (models.CharField, {'max_length': 255, 'default': '---'}),
    None,
    (models.TextField, {'null': True, 'blank': True}),
    (models.DateTimeField, {'null': True, 'blank': True}),
    (models.IntegerField, {}),
    None,
]


@python_2_unicode_compatible
class FieldDef(models.Model):
    name = models.CharField(max_length=64)
    type = models.IntegerField(default=0, choices=CF_TYPE_CHOICES)
    custom = models.SmallIntegerField(default=0)
    description = models.CharField(max_length=255)
    long_desc = models.CharField(max_length=255, default='')
    mailhead = models.SmallIntegerField(default=0)
    sortkey = models.IntegerField()
    obsolete = models.SmallIntegerField(default=0)
    enter_bug = models.SmallIntegerField(default=0)
    buglist = models.SmallIntegerField(default=0)
    visibility_field = models.ForeignKey('self', blank=True, null=True, related_name='+')
    value_field = models.ForeignKey('self', blank=True, null=True, related_name='+')
    reverse_desc = models.CharField(max_length=255, blank=True, null=True)
    mandatory = models.SmallIntegerField(default=0, db_column='is_mandatory')
    numeric = models.SmallIntegerField(default=0, db_column='is_numeric')

    class Meta:
        db_table = 'fielddefs'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class BaseBugField(models.Model):
    value = models.CharField(max_length=64)
    sortkey = models.IntegerField(default=0)
    active = models.SmallIntegerField(default=0, db_column='isactive')
    visibility_value_id = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.value


@python_2_unicode_compatible
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, db_index=True, unique=True)
    classification_id = models.SmallIntegerField(default=1)
    description = models.TextField(null=True)
    isactive = models.SmallIntegerField(default=1)
    defaultmilestone = models.CharField(max_length=64, default='---')
    allows_unconfirmed = models.SmallIntegerField(default=1)

    class Meta:
        db_table = 'products'
        ordering = ['name']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Component(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, db_index=True)
    product = models.ForeignKey('project.Product')
    owner = models.ForeignKey('user.Profile', db_index=False,
        db_column='initialowner', related_name='owned_components')
    qa = models.ForeignKey('user.Profile', null=True,
        db_column='initialqacontact', related_name='watched_compononets')
    description = models.TextField(default='')
    active = models.BooleanField(db_column='isactive', default=True)
    cc = models.ManyToManyField('user.Profile',
        related_name='components', through='ComponentCC',
        null=True, blank=True)

    class Meta:
        db_table = 'components'
        unique_together = ('name', 'product')

    def __str__(self):
        return self.name


class ComponentCC(models.Model):
    id = db.MultiFieldPK("user", "component")
    user = models.ForeignKey('user.Profile', db_column='user_id', related_name='+')
    component = models.ForeignKey(Component, db_column='component_id', related_name='+')

    class Meta:
        db_table = 'component_cc'
        auto_created = Component


@python_2_unicode_compatible
class Version(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=64)
    product = models.ForeignKey('project.Product')
    active = models.SmallIntegerField(default=1)

    class Meta:
        db_table = 'versions'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Milestone(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('project.Product')
    value = models.CharField(max_length=64)
    sortkey = models.IntegerField(default=0)
    active = models.SmallIntegerField(default=1, db_column='isactive')

    class Meta:
        db_table = 'milestones'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Status(BaseBugField):
    is_open = models.BooleanField(default=True)

    class Meta:
        db_table = 'bug_status'
        ordering = ['sortkey', 'value']

    def __str__(self):
        return self.value


@python_2_unicode_compatible
class Severity(BaseBugField):
    class Meta:
        db_table = 'bug_severity'
        ordering = ['sortkey', 'value']

    def __str__(self):
        return self.value


@python_2_unicode_compatible
class Resolution(BaseBugField):
    class Meta:
        db_table = 'resolution'
        ordering = ['sortkey', 'value']

    def __str__(self):
        return self.value


@python_2_unicode_compatible
class Priority(BaseBugField):
    class Meta:
        db_table = 'priority'
        ordering = ['sortkey', 'value']

    def __str__(self):
        return self.value


@python_2_unicode_compatible
class OS(BaseBugField):
    class Meta:
        db_table = 'op_sys'
        ordering = ['sortkey', 'value']

    def __str__(self):
        return self.value


@python_2_unicode_compatible
class Domain(BaseBugField):
    class Meta:
        db_table = 'rep_platform'
        ordering = ['sortkey', 'value']

    def __str__(self):
        return self.value


@python_2_unicode_compatible
class BaseBug(models.Model):
    '''Bugzilla bug'''

    class Meta:
        abstract = True

    def __str__(self):
        return '#%s' % self.id

    id = models.AutoField(primary_key=True, db_column='bug_id')
    alias = models.CharField(max_length=20, db_index=True, unique=True, null=True, blank=True)
    title = models.CharField(max_length=255, db_column='short_desc')
    assignee = models.ForeignKey('user.Profile', db_column='assigned_to')
    product = models.ForeignKey('project.Product', default=None, db_index=True)

    component = models.ForeignKey('project.Component',
        blank=True, null=True, default=None)

    version = models.CharField(max_length=64, default='', db_index=True)
    milestone = models.CharField(max_length=64, db_index=True,
        db_column='target_milestone', default='---')

    bug_file_loc = models.TextField(default='', blank=True)
    severity = models.CharField(max_length=64,
        db_column='bug_severity', db_index=True)
    status = models.CharField(max_length=64,
        db_column='bug_status', db_index=True)
    resolution = models.CharField(max_length=64, default='', blank=True, db_index=True)
    priority = models.CharField(max_length=64, db_index=True)

    dependson = models.ManyToManyField('self',
        related_name='blocked', through='BugDependencies',
        null=True, blank=True, symmetrical=False)

    cc = models.ManyToManyField('user.Profile',
        related_name='cc_bugs', through='BugCC',
        null=True, blank=True)
    cclist_accessible = models.SmallIntegerField(default=1)

    creation_ts = models.DateTimeField(db_index=True, null=True, auto_now_add=True)
    delta_ts = models.DateTimeField(auto_now=True, db_index=True)
    lastdiffed = models.DateTimeField(null=True, blank=True, default=None)
    deadline = models.DateTimeField(null=True)

    estimated_time = models.DecimalField(max_digits=5,
        decimal_places=2, default='0')
    remaining_time = models.DecimalField(max_digits=5,
        decimal_places=2, default='0')

    everconfirmed = models.SmallIntegerField(default=0)

    os = models.CharField(max_length=64, db_index=True, db_column='op_sys')
    domain = models.CharField(max_length=64, db_column='rep_platform')

    reporter = models.ForeignKey('user.Profile', db_column='reporter',
        related_name='created_bugs')

    reporter_accessible = models.SmallIntegerField(default=1)
    status_whiteboard = models.TextField(default='')


def create_bug_model(class_name=None, options=None):
    """
    Enrich the BaseBug to use the custom bugzilla fields
    Inspiration from https://code.djangoproject.com/wiki/DynamicModels
    """
    class Meta:
        db_table = 'bugs'
        app_label = 'project'        

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': 'project', 'Meta': Meta}

    # Add in any fields that were provided
    try:
        for field_def in FieldDef.objects.filter(custom=True, obsolete=False):
            try:
                FieldClass, options = CF_TYPE_MAPPING[field_def.type]
            except TypeError:
                print('Skipping field %s' % field_def)
                continue
            attrs.update({field_def.name: FieldClass(**options)})
    except Exception as e:
        print('Exception caught: %s' % str(e))

    # Create the class, which automatically triggers ModelBase processing
    model = type(class_name or str('Bug'), (BaseBug,), attrs)

    return model


Bug = create_bug_model()


@python_2_unicode_compatible
class BugDependencies(models.Model):
    id = db.MultiFieldPK("blocked", "dependson")
    blocked = models.ForeignKey(Bug, db_column='blocked', related_name='+')
    dependson = models.ForeignKey(Bug, db_column='dependson', related_name='+')

    class Meta:
        db_table = 'dependencies'
        auto_created = Bug

    def __str__(self):
        return '%i -> %i' % (self.dependson_id, self.blocked_id)


@python_2_unicode_compatible
class BugCC(models.Model):
    id = db.MultiFieldPK("bug", "who")
    bug = models.ForeignKey(Bug, db_column='bug_id', related_name='+')
    who = models.ForeignKey('user.Profile', db_column='who', related_name='+')

    class Meta:
        db_table = 'cc'
        auto_created = Bug

    def __str__(self):
        return '%i -> %i' % (self.who_id, self.bug_id)


@python_2_unicode_compatible
class Comment(models.Model):
    id = models.AutoField(primary_key=True, db_column='comment_id')
    bug = models.ForeignKey('project.Bug', related_name='comments',
        to_field='id', db_column='bug_id', db_index=True)
    who = models.ForeignKey('user.Profile',
        to_field='id', db_column='who', db_index=True)
    bug_when = models.DateTimeField(auto_now_add=True, db_index=True)
    work_time = models.DecimalField(default='0.00',
        max_digits=5, decimal_places=2)
    content = models.TextField(db_column='thetext')
    private = models.SmallIntegerField(default=0, db_column='isprivate')
    already_wrapped = models.SmallIntegerField(default=0)
    type = models.IntegerField(default=0)
    extra_data = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'longdescs'

    def __str__(self):
        return self.content
