
import pytest
from bughipster.bz_admin import views
from bughipster.project import models


pytestmark = pytest.mark.django_db


# TODO: add the add product tests


def test_edit_product_without_selecting_product(rf):
    request = rf.get('editproducts.cgi?action=edit')
    response = views.Products.as_view()(request)
    assert 'message' in response.context_data
    assert 'You must select/enter a product.' in response.context_data['message']
    assert response.template_name == 'error.html'


def test_edit_product_that_does_not_exist(rf):
    request = rf.get('editproducts.cgi?action=edit&product=ekjzri')
    response = views.Products.as_view()(request)
    assert 'message' in response.context_data
    assert "Either the product 'ekjzri' does not exist or you don't have access to it." in response.context_data['message']
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
    response = views.Products.as_view()(request)
    assert response.status_code == 200
    assert response.template_name == 'bz_admin/products/changes_summary.html'
    assert response.context_data['changes'] == expected_changes
    product = models.Product.objects.get(id=product.id)
    assert product.description == new_description
    assert not product.isactive
