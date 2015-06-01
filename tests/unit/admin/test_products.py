
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
    models.Product.objects.create(
        name='someproduct',
        description='Some product description.',
    )
    request = rf.get('editproducts.cgi?action=edit&product=ekjzri')
    response = views.Products.as_view()(request)
    assert 'message' in response.context_data
    assert "Either the product 'ekjzri' does not exist or you don't have access to it." in response.context_data['message']
    assert response.template_name == 'error.html'
