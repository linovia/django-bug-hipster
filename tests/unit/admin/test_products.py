"""
tests.unit.admin.test_products
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2015 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import pytest
from bughipster.bz_admin import views
from bughipster.project import models
from bughipster.user import factories as user_factories


pytestmark = pytest.mark.django_db


def test_list_product(rf):
    request = rf.get('editproducts.cgi')
    response = views.products(request)
    assert response.status_code == 200


def test_create_product(rf):
    user_factories.Profile.create(login_name='xordoquy@linovia.com')
    request = rf.post('editproducts.cgi?action=add', {
        'product': "somedemo",
        'description': "some description",
        'is_active': "1",
        'allows_unconfirmed': "on",
        'version': "unspecified",
        'createseries': "1",
        'component': "comp",
        'comp_desc': "component description",
        'initialowner': "xordoquy@linovia.com",
        'initialcc': "",
        'action': "new",
        'classification': "",
    })
    response = views.products(request)
    assert response.status_code == 200
    assert response.template_name == 'bz_admin/products/edit.html'
    product = models.Product.objects.all()
    assert len(product) == 1
    product = product[0]
    assert models.Component.objects.filter(product=product).exists()
    assert models.Version.objects.filter(product=product).exists()


def test_create_product_with_unknown_owner(rf):
    request = rf.post('editproducts.cgi?action=add', {
        'product': "somedemo",
        'description': "some description",
        'is_active': "1",
        'allows_unconfirmed': "on",
        'version': "unspecified",
        'createseries': "1",
        'component': "comp",
        'comp_desc': "component description",
        'initialowner': "xordoquy@linovia.com",
        'initialcc': "",
        'action': "new",
        'classification': "",
    })
    response = views.products(request)
    assert response.status_code == 200
    assert response.template_name == 'error.html'
    product = models.Product.objects.all()
    assert len(product) == 0
    print(response.context_data['message'])
    assert (
        'Bugzilla was unable to make any match at all for one or more '
        'of the names and/or email addresses you entered on the previous '
        'page.') in response.context_data['message']


#
# ADMIN EDIT PRODUCT
#

def test_edit_product_without_selecting_product(rf):
    request = rf.get('editproducts.cgi?action=edit')
    response = views.products(request)
    assert 'message' in response.context_data
    assert 'You must select/enter a product.' in \
        response.context_data['message']
    assert response.template_name == 'error.html'


def test_edit_product_that_does_not_exist(rf):
    request = rf.get('editproducts.cgi?action=edit&product=ekjzri')
    response = views.products(request)
    assert 'message' in response.context_data
    expected_result = (
        "Either the product 'ekjzri' does not exist "
        "or you don't have access to it.")
    assert expected_result in response.context_data['message']
    assert response.template_name == 'error.html'


def test_edit_product(rf):
    product = models.Product.objects.create(
        name='someproduct',
        description='Some product description.',
    )
    new_description = 'Another description'
    request = rf.post('editproducts.cgi?action=edit&product=someproduct', {
        'product': 'someproduct',
        'description': new_description,
        # 'is_active': ,
        'allows_unconfirmed': 'on',
    })
    expected_changes = {
        'description': {
            'new': 'Another description',
            'old': 'Some product description.'
        },
        'isactive': {
            'new': False,
            'old': 1
        }
    }
    response = views.products(request)
    assert response.status_code == 200
    assert response.template_name == 'bz_admin/products/changes_summary.html'
    assert response.context_data['changes'] == expected_changes
    product = models.Product.objects.get(id=product.id)
    assert product.description == new_description
    assert not product.isactive


def test_edit_product_with_empty_name(rf):
    models.Product.objects.create(
        name='someproduct',
        description='Some product description.',
    )
    request = rf.post('editproducts.cgi?action=edit&product=someproduct', {
        'product': '',
    })
    response = views.products(request)
    assert response.status_code == 200
    assert response.template_name == 'error.html'
    assert response.context_data['message'] == \
        "You must enter a name for the product."


#
# ADMIN DELETE PRODUCT
#

def test_delete_product_get_with_no_product(rf):
    request = rf.get('editproducts.cgi?action=del')
    response = views.products(request)
    assert response.status_code == 200
    assert response.template_name == 'error.html'
    assert response.context_data['message'] == \
        "You must select/enter a product."


def test_delete_product_get_with_unknown_product(rf):
    request = rf.get('editproducts.cgi?action=del&product=toto')
    response = views.products(request)
    assert response.status_code == 200
    assert response.template_name == 'error.html'
    assert response.context_data['message'] == (
        "Either the product 'toto' does not exist "
        "or you don't have access to it."
    )
