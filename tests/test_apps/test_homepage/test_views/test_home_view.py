from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse


@pytest.mark.django_db(transaction=True)
def test_home_page(client: Client):
    """This test ensures that home page works."""
    response = client.get(reverse('homepage:home'))

    assert 'product_page' in response.context
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db(transaction=True)
def test_page_not_found_home_page(client: Client):
    """This test ensures that home page raise 404."""
    response = client.get('/?page=10')

    assert response.status_code == HTTPStatus.NOT_FOUND
