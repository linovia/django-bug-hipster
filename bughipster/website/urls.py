"""
bughipster.website.urls
~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django.conf.urls import include, url
from . import views
from bughipster.project import views as project_views


front_urls = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^index\.cgi$', views.Home.as_view(), name='home'),
    url(r'^enter_bug\.cgi$', project_views.bug_creation, name='create-bug'),
    url(r'^query\.cgi$', views.query, name='view-query'),
    url(r'^buglist\.cgi$', project_views.BugList.as_view(), name='list-bug'),

    # TODO:
    url(r'^describecomponents\.cgi$', views.ToDo.as_view(), name='view-component'),
    url(r'^duplicates\.cgi$', views.ToDo.as_view(), name='duplicates'),
    url(r'^page\.cgi$', views.ToDo.as_view(), name='flatpage'),
    url(r'^report\.cgi$', views.ToDo.as_view(), name='view-report'),
    url(r'^search_plugin\.cgi$', views.ToDo.as_view(), name='search-plugin'),
    url(r'^show_bug\.cgi$', views.ToDo.as_view(), name='bug-details'),
]

user_urls = [
    url(r'^createaccount\.cgi$', views.CreateAccount.as_view(), name='create-account'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),

    # TODO:
    url(r'^userprefs\.cgi$', views.ToDo.as_view(), name='prefs'),
    url(r'^forgot_password/$', views.ToDo.as_view(), name='forgot-password'),
]

urlpatterns = [
    url(r'', include(front_urls, namespace='front')),
    url(r'', include(user_urls, namespace='user')),
]
