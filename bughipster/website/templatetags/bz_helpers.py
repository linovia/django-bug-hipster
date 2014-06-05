"""
bughispster.website.templatetags.bz_helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2013-2014 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from __future__ import unicode_literals

from django import template
from django.utils.http import urlencode
from django.template.defaultfilters import stringfilter
from django.utils.text import Truncator

register = template.Library()


@register.simple_tag
def create_filtered_query_string(request):
    striped_query = dict([(k, v) for k, v in request.GET.items() if v])

    # TODO: Why do I need this ?
    striped_query.pop('no_redirect', None)

    # TODO: add extra arguments if needed
    # In particular list_id for bug lists
    return urlencode(striped_query)


#
# Custom truncator
#

class BzTruncator(Truncator):
    def add_truncation_text(self, text, truncate=None):
        return text


@register.filter(is_safe=True)
@stringfilter
def raw_truncate_chars(value, arg):
    """
    Truncates a string after a certain number of characters.

    Argument: Number of characters to truncate after
    """
    try:
        length = int(arg)
    except ValueError: # Invalid literal for int()
        return value
    return BzTruncator(value).chars(length)
