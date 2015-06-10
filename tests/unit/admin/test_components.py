"""
tests.unit.admin.test_components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2015 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import pytest
from bughipster.bz_admin import views
from bughipster.project import models
from bughipster.user import factories as user_factories


pytestmark = pytest.mark.django_db


def test_choose_product(rf):
    request = rf.get('editcomponents.cgi')
    response = views.products(request)
    assert response.status_code == 200
    assert response.template_name == 'bz_admin/components/product_choice.html'


def test_list_components_for_unknown_product(rf):
    request = rf.get('editcomponents.cgi?product=toto')
    response = views.products(request)
    assert response.status_code == 200
    assert response.template_name == 'errors.html'
    assert response.context_data['message'] == (
        "Either the product 'toto' does not exist or you don't "
        "have access to it.")
