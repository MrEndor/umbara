from http import HTTPStatus

from django.test.client import Client
from django.urls import reverse


def test_item_list_page(client: Client, catalog_list_items_body: str):
    """This test ensures that item list page works."""
    response = client.get(reverse('catalog:item_list'))

    assert response.status_code == HTTPStatus.OK
    assert response.content.decode() == catalog_list_items_body
