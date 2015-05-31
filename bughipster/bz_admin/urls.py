"""
bughipster.bz_admin.urls
~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2015 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django.conf.urls import url
from bughipster.website.views import ToDo
from . import views

urlpatterns = [
    url(r'^admin\.cgi$', views.Index.as_view(), name='index'),

    url(r'^editparams\.cgi$', ToDo.as_view(), name='params'),
    url(r'^editsettings\.cgi$', ToDo.as_view(), name='settings'),
    url(r'^sanitycheck\.cgi$', ToDo.as_view(), name='sanitycheck'),
    url(r'^editusers\.cgi$', ToDo.as_view(), name='users'),
    url(r'^editclassifications\.cgi$', ToDo.as_view(), name='classifications'),
    url(r'^editproducts\.cgi$', ToDo.as_view(), name='products'),
    url(r'^editcomponents\.cgi$', ToDo.as_view(), name='components'),
    url(r'^editversions\.cgi$', ToDo.as_view(), name='versions'),
    url(r'^editmilestones\.cgi$', ToDo.as_view(), name='milestones'),
    url(r'^editflagtypes\.cgi$', ToDo.as_view(), name='flagtypes'),
    url(r'^editfields\.cgi$', ToDo.as_view(), name='fields'),
    url(r'^editvalues\.cgi$', ToDo.as_view(), name='values'),
    url(r'^editworkflow\.cgi$', ToDo.as_view(), name='workflow'),
    url(r'^editgroups\.cgi$', ToDo.as_view(), name='groups'),
    url(r'^editkeywords\.cgi$', ToDo.as_view(), name='keywords'),
    url(r'^editwhines\.cgi$', ToDo.as_view(), name='whines'),
]
