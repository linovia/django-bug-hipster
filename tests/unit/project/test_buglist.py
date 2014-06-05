"""
test_buglist
~~~~~~~~~~~~

Tests the various bug list filters
"""

import pytest

from django.test.client import RequestFactory

from bughipster.project.models import Bug
from bughipster.project import models, factories, views


@pytest.mark.django_db
def test_bug_queryset_with_status():
    # Status creation
    models.Status.objects.create(value='NEW', is_open=True)
    models.Status.objects.create(value='CLOSED', is_open=False)

    # Create an opened and a closed bug
    bug = factories.Bug.create()
    bug.status = 'NEW'
    bug.save()
    bug2 = factories.Bug.create(
        product=bug.product,
        assignee=bug.assignee,
        reporter=bug.reporter)
    bug2.status = 'CLOSED'
    bug2.save()

    # Assertions
    assert Bug.objects.count() == 2
    opened = list(Bug.objects.opened())
    assert len(opened) == 1
    assert opened[0].id == bug.id
    closed = list(Bug.objects.closed())
    assert len(closed) == 1
    assert closed[0].id == bug2.id


@pytest.mark.django_db
def test_filter_on_bug_status():
    # Status creation
    models.Status.objects.create(value='NEW', is_open=True)
    models.Status.objects.create(value='CLOSED', is_open=False)

    # Create an opened and a closed bug
    bug1 = factories.Bug.create()
    bug1.status = 'NEW'
    bug1.save()
    bug2 = factories.Bug.create(
        product=bug1.product,
        assignee=bug1.assignee,
        reporter=bug1.reporter)
    bug2.status = 'CLOSED'
    bug2.save()

    rf = RequestFactory()

    # Make sure bug_status also works with regular status

    # Test with bug_status either NEW or CLOSED
    request = rf.get('buglist.cgi?bug_status=NEW&bug_status=CLOSED')
    response = views.BugList.as_view()(request)
    bug_list = response.context_data['bug_list']
    assert len(bug_list) == 2

    # Test with bug_status=NEW
    request = rf.get('buglist.cgi?bug_status=NEW')
    response = views.BugList.as_view()(request)
    bug_list = response.context_data['bug_list']
    assert len(bug_list) == 1
    assert bug_list[0].title == bug1.title

    # Test with bug_status=CLOSED
    request = rf.get('buglist.cgi?bug_status=CLOSED')
    response = views.BugList.as_view()(request)
    bug_list = response.context_data['bug_list']
    assert len(bug_list) == 1
    assert bug_list[0].title == bug2.title

    # The 3 tests here are for Bugzilla compatibility with simple search

    # Test with bug_status=__open__
    request = rf.get('buglist.cgi?bug_status=__open__')
    response = views.BugList.as_view()(request)
    bug_list = response.context_data['bug_list']
    assert len(bug_list) == 1
    assert bug_list[0].title == bug1.title

    # Test with bug_status=__closed__
    request = rf.get('buglist.cgi?bug_status=__closed__')
    response = views.BugList.as_view()(request)
    bug_list = response.context_data['bug_list']
    assert len(bug_list) == 1
    assert bug_list[0].title == bug2.title

    # Test with bug_status=__all__
    request = rf.get('buglist.cgi?bug_status=__all__')
    response = views.BugList.as_view()(request)
    bug_list = response.context_data['bug_list']
    assert len(bug_list) == 2

    # Test with an empty bug status
    request = rf.get('buglist.cgi?bug_status=')
    response = views.BugList.as_view()(request)
    bug_list = response.context_data['bug_list']
    assert len(bug_list) == 2
