"""
bughipster.website.urls
~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Xavier Ordoquy,
see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django.conf.urls import patterns, include, url
from . import views
from bughipster.project import views as project_views


urlpatterns = patterns('',
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^index\.cgi$', views.Home.as_view(), name='home'),
    url(r'^createaccount\.cgi$', views.CreateAccount.as_view(), name='create-account'),
    url(r'^enter_bug\.cgi$', project_views.bug_creation, name='create-bug'),

    # TODO:
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
)
