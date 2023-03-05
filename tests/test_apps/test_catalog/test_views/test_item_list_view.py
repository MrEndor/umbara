from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse


@pytest.mark.django_db()
def test_item_list_page(client: Client, tmp_path_factory):
    """This test ensures that item list page works."""
    response = client.get(reverse('catalog:item_list'))

    assert 'product_page' in response.context
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db(transaction=True)
def test_page_not_found_item_list_page(client: Client, tmp_path_factory):
    """This test ensures that item list page raise 404."""
    response = client.get('/catalog/?page=10')

    assert response.status_code == HTTPStatus.NOT_FOUND
