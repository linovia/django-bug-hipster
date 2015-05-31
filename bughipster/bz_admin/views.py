"""
bughipster.bz_admin.views
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2015 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django.views import generic


class Index(generic.TemplateView):
    template_name = 'bz_admin/index.html'
