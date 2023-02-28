from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse


@pytest.mark.django_db()
def test_item_list_page(client: Client):
    """This test ensures that item list page works."""
    response = client.get(reverse('catalog:item_list'))

    assert response.status_code == HTTPStatus.OK
